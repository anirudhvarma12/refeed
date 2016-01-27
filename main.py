from flask import Flask
from flask import render_template

from models import db,FeedItem
import rss

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.debug = True
db.init_app(app)


@app.before_first_request
def create_database():
    print("attempting database creation")
    # db.create_all()
    # item1 = FeedItem("http://stackoverflow.com/questions/13213048/urllib2-http-error-429")
    # item2 = FeedItem("http://flask-sqlalchemy.pocoo.org/2.1/quickstart/")
    # db.session.add(item1)
    # db.session.add(item2)
    # db.session.commit()


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/feed")
def get_feed():
    return rss.get_rss()

if __name__ == "__main__":
    app.run()
