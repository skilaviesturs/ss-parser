# This script fetches the RSS feed from ss.lv and parses it to extract relevant information.

import ss_feed
from db_utils import save_entries_to_db, Session, Entry
from config import SS_RSS_URL
import web_utils
import listing_analyzer
import notifier

def main():
    entries = ss_feed.fetch_ss_rss_feed(SS_RSS_URL)
    # Save entries and count new ones
    session = Session()
    new_count = 0
    for entry in entries:
        exists = session.query(Entry).filter_by(link=entry.get('link')).first()
        if not exists:
            db_entry = Entry(
                title=entry.get('title'),
                link=entry.get('link'),
                published=entry.get('published'),
                is_processed=False
            )
            session.add(db_entry)
            new_count += 1
    session.commit()
    # Analyze unprocessed entries
    unprocessed = session.query(Entry).filter_by(is_processed=False).all()
    match_count = 0
    for entry in unprocessed:
        try:
            soup = web_utils.fetch_and_parse(entry.link)
            is_match = listing_analyzer.analyze_listing(soup)
            entry.is_match = is_match
            entry.is_processed = True
            if is_match:
                notifier.notify_ntfy(entry.title, entry.link)
                match_count += 1
        except Exception:
            pass  # Silently ignore errors
    session.commit()
    session.close()
    print(f"New entries added: {new_count}")
    print(f"Matches found: {match_count}")

if __name__ == "__main__":
    main()