import web_utils
import listing_analyzer
import sys
import notifier
from notifier import generate_title

def test_listing(url):
    soup = web_utils.fetch_and_parse(url)
    is_match, data = listing_analyzer.analyze_listing(soup)
    data.pop('text', None)
    print("is_match:", is_match)
    print("parsed data:", data)
    if is_match:
        title = generate_title(data)
        notifier.notify_ntfy(title, url)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter SS.lv listing URL: ").strip()
    test_listing(url)
