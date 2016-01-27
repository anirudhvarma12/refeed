from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class FeedItem(db.Model):
    feedId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(400))
    date = db.Column(db.DateTime)

    def __init__(self, url):
        self.url = url
        self.date = datetime.datetime.now()
