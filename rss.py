from bs4 import BeautifulSoup
from models import FeedItem
import dbservice
import datetime
import PyRSS2Gen
import urllib
import settings


def get_feed_items():
    return dbservice.get_feed_items()


def get_rss():
    all_feeds = get_feed_items()
    size = len(all_feeds)
    rss = PyRSS2Gen.RSS2(
        title=settings.title, lastBuildDate=datetime.datetime.now(),
        link=settings.main_url, description=settings.description)
    for i in range(size):
        rss.items.append(convert(all_feeds[i]))
    return rss.to_xml()


def convert(item):
    return PyRSS2Gen.RSSItem(title=item.title, link=item.url, description=item.description, pubDate=item.date)


def get_feed_item(url, description, user_id):
    if description is None:
        description = ""
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozila/5.0"})
    client = urllib.request.urlopen(request)
    web_page = BeautifulSoup(client.read(), "html.parser")
    title = web_page.title.string
    return create_feed_item(url, description, user_id, title)


def create_feed_item(url, description, user_id, title):
    item = FeedItem(url, title)
    item.description = description
    item.user_id = user_id
    return item


def is_feed_allowed(existing_item_date, new_item_date):
    time_diff = new_item_date - existing_item_date
    days = time_diff.days
    print('Number of days ' + str(days))
    if days > 7:
        return True

    return False
