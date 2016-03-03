from flask import Flask, Response
from flask import render_template, request, session, redirect, url_for
import rss
import datetime
import dbservice
import math
import settings

app = Flask(__name__)
app.debug = True
app.secret_key = "something very secret should be set in production"
dbservice.bcrypt.init_app(app)


@app.route("/")
def index():
    total_count = dbservice.get_feed_count()
    current_page = request.args.get('page')
    numberOfPages = math.floor(total_count/5)
    if current_page is None:
        current_page = 5
    else:
        current_page = int(current_page)
    if current_page > numberOfPages:
        current_page = numberOfPages
    limit = (current_page-1) * 5
    list = dbservice.get_item_after(5, limit)
    prev_page = None
    if current_page >= 1:
        prev_page = current_page - 1
    if current_page == numberOfPages:
        current_page = None
    else:
        current_page = current_page+1
    return render_template("index.html", title=settings.title, count=dbservice.get_feed_count(), feeds=list, prev_page = prev_page, new_page = current_page)


@app.route("/feed")
def get_feed():
    feed = rss.get_rss()
    return Response(feed, mimetype='text/xml')


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
        description = ""
        existing_item = dbservice.get_feed_by_url(url)
        if existing_item is None:
            print("No existing feed item found")
            item = rss.get_feed_item(url, description, user.username)
            dbservice.store_item(item)
            error = "Success"
        elif rss.is_feed_allowed(existing_item.date, datetime.datetime.now()):
            item = rss.get_feed_item(url, description, user.username)
            dbservice.store_item(item)
            error = "Success"
        else:
            error = "Feed was added less than 7 days ago"
    return render_template("add_item.html", error=error)


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

    return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    if 'login' not in session:
        return redirect(url_for('login'))

    session.pop('login', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
