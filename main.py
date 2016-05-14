from flask import Flask, Response
from flask import render_template, request, session, redirect, url_for
import rss
from slack import execute_command, get_response
import dbservice
import math
import settings

app = Flask(__name__)
app.debug = True
app.secret_key = "something very secret should be set in production"
dbservice.bcrypt.init_app(app)


@app.route("/")
def index():
    ITEM_LIMIT = 20
    total_count = dbservice.get_feed_count()
    current_page = request.args.get('page')
    numberOfPages = math.ceil(total_count / ITEM_LIMIT)
    if current_page is None:
        current_page = 1
    else:
        current_page = int(current_page)
    if current_page > numberOfPages:
        current_page = numberOfPages
    limit = (current_page - 1) * ITEM_LIMIT
    list = dbservice.get_item_after(ITEM_LIMIT, limit)
    prev_page = None
    if current_page >= 1:
        prev_page = current_page - 1
    if current_page == numberOfPages:
        current_page = None
    else:
        current_page = current_page + 1
    return render_template("index.html", title=settings.title, count=total_count, feeds=list, prev_page=prev_page, new_page=current_page)


@app.route("/feed")
def get_feed():
    feed = rss.get_rss()
    return Response(feed, mimetype='text/xml')


def is_valid_title(title):
    if title is None:
        return False
    elif len(title) == 0:
        return False
    elif str(title).isspace():
        return False
    else:
        return True


@app.route("/add", methods=['GET', 'POST'])
def add():
    error = None
    if 'login' not in session:
        return redirect(url_for('login'))
    user = dbservice.get_user(username=session['login'])
    if user is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        url = request.form['url']
        description = request.form['description']
        title = request.form['title']
        try:
            result = rss.add_artcle(url, description, title, user)
            if result == rss.STATUS_OK:
                error = "Success"
            elif result == rss.STATUS_EXISTS:
                error = "Feed was added less than 7 days ago"
        except:
            error = 'Could not save'
    return render_template("add_item.html", error=error, title=settings.title)


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        if 'login' in session:
            return redirect(url_for('add'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = dbservice.authenticate(username, password)
        if user is None:
            error = "User not exists"
        elif user:
            session['login'] = user.username
            return redirect(url_for('add'))
        else:
            error = "Could not authenticate"

    return render_template("login.html", error=error, title=settings.title)


@app.route('/logout')
def logout():
    if 'login' not in session:
        return redirect(url_for('login'))

    session.pop('login', None)
    return redirect(url_for('index'))


@app.route("/slack", methods=['POST'])
def handle_slack():
    if settings.slack_token is None or settings.slack_user is None:
        return get_response('Error: Slack configuration not found')
    token = request.form['token']
    print('Got token ' + token + " given " + settings.slack_token)
    if settings.slack_token != token:
        return get_response('Error: Slack token does not match')
    user = dbservice.get_user(settings.slack_user)
    if user is None:
        return get_response('Error: Slack user does not exist')
    text = request.form['text']
    if text is not None:
        return execute_command(text, user)
    else:
        return get_response("No Command Found")

if __name__ == "__main__":
    app.run()
