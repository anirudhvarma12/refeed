from flask_bcrypt import Bcrypt
from models import User, FeedItem
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from models import Base
import settings

engine = create_engine("sqlite:///" + settings.db_path)
Session = sessionmaker()
Session.configure(bind=engine)
bcrypt = Bcrypt()

PAGE_SIZE = 25


def create_db():
    Base.metadata.create_all(engine)


def add_user(username, password):
    session = Session()
    pw_hashed = bcrypt.generate_password_hash(password)
    user = User(username, pw_hashed)
    session.add(user)
    session.commit()


def get_user(username):
    session = Session()
    query = (session.query(User).filter_by(username=username))
    return query.first()


def authenticate(username, password):
    user = get_user(username)
    if(user is None):
        return None
    else:
        print("Comparing password for " + user.username)
        if bcrypt.check_password_hash(user.password, password):
            return user
    return False


def get_feed_items():
    session = Session()
    query = (session.query(FeedItem).order_by(desc(FeedItem.date)))
    return query.limit(PAGE_SIZE).all()


def get_item_after(startId, offset):
    session = Session()
    query = (session.query(FeedItem).order_by(desc(FeedItem.date)))
    return query.limit(startId).offset(offset).all()


def get_feed_by_url(url):
    session = Session()
    query = (session.query(FeedItem).filter_by(url=url))
    return query.first()


def store_item(feed_item):
    session = Session()
    session.add(feed_item)
    session.commit()


def get_feed_count():
    session = Session()
    return session.query(FeedItem).count()


def get_random():
    session = Session()
    return session.query(FeedItem).order_by(func.random()).first()