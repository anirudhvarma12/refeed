from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class FeedItem(Base):
    __tablename__ = "feed_items"
    feedId = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(400))
    date = Column(DateTime)
    title = Column(String(255))
    description = Column(String(500))
    user_id = Column(String, ForeignKey("users.username"))

    def __init__(self, url, title):
        self.url = url
        self.date = datetime.datetime.now()
        self.title = title


class User(Base):
    __tablename__ = "users"
    username = Column(String(250), primary_key=True)
    password = Column(String(250))
    items = relationship("FeedItem")

    def __init__(self, name, password):
        self.username = name
        self.password = password


class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    main_url = Column(String(400))
    description = Column(String(400))
    title = Column(String(255))
