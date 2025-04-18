import requests
import feedparser

def fetch_ss_rss_feed(rss_url):
    response = requests.get(rss_url)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    return feed.entries
