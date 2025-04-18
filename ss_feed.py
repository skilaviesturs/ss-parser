import requests
import feedparser

def fetch_ss_rss_feed(rss_url):
    """
    Downloads and parses the given RSS feed URL from ss.lv.
    Returns a list of feed items (each as a dict).
    """
    response = requests.get(rss_url)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    return feed.entries
