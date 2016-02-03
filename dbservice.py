from main import app
from flask_bcrypt import Bcrypt
from models import User, FeedItem
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from models import Base
import settings

engine = create_engine("sqlite:///"+settings.db_path)
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
        if bcrypt.check_password_hash(user.password, password):
            return user
    return False


def get_feed_items():
    query = (session.query(FeedItem).order_by(desc(FeedItem.date)))
    query.limit(25)
    return query.all()


def get_feed_by_url(url):
    query = (session.query(FeedItem).filter_by(url=url))
    return query.first()


def store_item(feed_item):
    session.add(feed_item)
    session.commit()


def get_settings():
    settings = session.query(Settings).first()
    if settings is None:
        settings = Settings()
    return settings


def set_main_url(url):
    settings = get_settings()
    settings.main_url = url
    session.add(settings)
    session.commit()


def set_description(desc):
    settings = get_settings()
    settings.description = desc
    session.add(settings)
    session.commit()


def set_title(title):
    settings = get_settings()
    settings.title = title
    session.add(settings)
    session.commit()


def get_feed_count():
    return session.query(FeedItem).count()
