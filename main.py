from flask import Flask
from flask import render_template, request
import rss
import datetime
import dbservice

app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/feed")
def get_feed():
    return rss.get_rss()


@app.route("/add", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = dbservice.authenticate(username, password)
        if user is None:
            error = "User not exists"
        elif user:
            url = request.form['url']
            #description = request.form['description']
            description = ""
            existing_item = dbservice.get_feed_by_url(url)
            if existing_item is None:
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

if __name__ == "__main__":
    app.run()
