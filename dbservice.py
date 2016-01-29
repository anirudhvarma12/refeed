from main import app
from flask_bcrypt import Bcrypt
from models import User, FeedItem
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///test.db")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
bcrypt = Bcrypt(app)


def create_db():
    Base.metadata.create_all(engine)


def add_user(username, password):
    pw_hashed = bcrypt.generate_password_hash(password)
    user = User(username, pw_hashed)
    session.add(user)
    session.commit()


def get_user(username):
    query = (session.query(User).filter_by(username=username))
    return query.first()


def authenticate(username, password):
    user = get_user(username)
    if(user is None):
        return None
    else:
        print("Comparing password for " + user.username)
        return bcrypt.check_password_hash(user.password, password)


def get_feed_items():
    query = (session.query(FeedItem).order_by(desc(FeedItem.date)))
    return query.all()


def get_feed_by_url(url):
    query = (session.query(FeedItem).filter_by(url=url))
    return query.first()


def store_item(feed_item):
    session.add(feed_item)
    session.commit()
