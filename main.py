from flask import Flask
from flask import render_template, request
import rss
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
        result = dbservice.authenticate(username, password)
        if result is None:
            error = "User not exists"
        elif result:
            error = "Success"
        else:
            error = "Could not authenticate"

    return render_template("add_item.html", error=error)

if __name__ == "__main__":
    app.run()
