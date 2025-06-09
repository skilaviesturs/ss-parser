import feedparser

def fetch_ss_rss_feed(url):
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        entries.append({
            'title': entry.get('title'),
            'link': entry.get('link'),
            'published': entry.get('published')
        })
    return entries
