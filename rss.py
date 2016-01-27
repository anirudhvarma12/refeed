from bs4 import BeautifulSoup
from models import FeedItem


def get_feed_items():
    return FeedItem.query.all()

# def get_rss():
# 	all_feeds = get_feed_items()
# 	size = len(all_feeds)
# 	for i in range(size):
# 		soup = BeautifulSoup()