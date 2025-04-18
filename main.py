# This script fetches the RSS feed from ss.lv and parses it to extract relevant information.

import ss_feed
from db_utils import save_entries_to_db, Session, Entry
from config import SS_RSS_URL
import web_utils
import listing_analyzer
import notifier

def main():
    entries = ss_feed.fetch_ss_rss_feed(SS_RSS_URL)
    save_entries_to_db(entries)
    # Analyze unprocessed entries
    session = Session()
    unprocessed = session.query(Entry).filter_by(is_processed=False).all()
    for entry in unprocessed:
        try:
            soup = web_utils.fetch_and_parse(entry.link)
            is_match = listing_analyzer.analyze_listing(soup)
            entry.is_match = is_match
            entry.is_processed = True
            if is_match:
                notifier.notify_ntfy(entry.title, entry.link)
        except Exception as e:
            pass  # Silently ignore errors
    session.commit()
    session.close()

if __name__ == "__main__":
    main()