from flask import Flask
from flask import render_template, request, session, redirect, url_for
import rss
import datetime
import dbservice
import settings

app = Flask(__name__)
app.debug = True
app.secret_key = "something very secret should be set in production"


@app.route("/")
def index():
    return render_template("index.html", title=settings.title, count=dbservice.get_feed_count())


@app.route("/feed")
def get_feed():
    return rss.get_rss()


@app.route("/add", methods=['GET', 'POST'])
def add():
    error = None
    if 'login' not in session:
        return redirect(url_for('login'))
    user = dbservice.get_user(username=session['login'])
    if user is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = dbservice.authenticate(username, password)
        if user is None:
            error = "User not exists"
        elif user:
            url = request.form['url']
            description = request.form['description']
            description = ""
            existing_item = dbservice.get_feed_by_url(url)
            if existing_item is None:
                print("No existing feed item found")
                item = rss.get_feed_item(url, description, user)
                dbservice.store_item(item)
                error = "Success"
            elif rss.is_feed_allowed(existing_item.date, datetime.datetime.now()):
                item = rss.get_feed_item(url, description, user)
                dbservice.store_item(item)
                error = "Success"
            else:
                error = "Feed was added less than 7 days ago"
        else:
            error = "Could not authenticate"

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


if __name__ == "__main__":
    app.run()
