from bs4 import BeautifulSoup
from models import FeedItem
import datetime
import PyRSS2Gen
import urllib


def get_feed_items():
    return FeedItem.query.all()


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
