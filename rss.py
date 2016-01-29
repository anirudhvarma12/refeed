from bs4 import BeautifulSoup
from models import FeedItem
import dbservice
import datetime
import PyRSS2Gen
import urllib


def get_feed_items():
    return dbservice.get_feed_items()


def get_rss():
    all_feeds = get_feed_items()
    size = len(all_feeds)
    rss = PyRSS2Gen.RSS2(
        title="Devs and Hackers Feed", lastBuildDate=datetime.datetime.now(),
        link="foo", description="ffee")
    for i in range(size):
        rss.items.append(convert(all_feeds[i]))

    return rss.to_xml()


def convert(item):
    print("Parsing item " + item.url)
    request = urllib.request.Request(
        item.url, headers={"User-Agent": "Mozila/5.0"})
    client = urllib.request.urlopen(request)
    soup = BeautifulSoup(client.read(), "html.parser")
    return PyRSS2Gen.RSSItem(title=soup.title.string, link=item.url, description="")


def get_feed_item(url, description, user_id):
    if description is None:
        description = ""
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozila/5.0"})
    client = urllib.request.urlopen(request)
    web_page = BeautifulSoup(client.read(), "html.parser")
    title = web_page.title.string
    item = FeedItem(url, title)
    item.description = description
    item.user_id = user_id
    return item


def is_feed_allowed(existing_item_date, new_item_date):
    time_diff = existing_item_date.date - new_item_date.date
    days = time_diff.days
    if days < 7:
        return True

    return False
