import ss_feed
from db_utils import save_entries_to_db, Session, Entry
from config import SS_RSS_URL
import web_utils
import listing_analyzer
import notifier
from notifier import generate_title

def run_parser():
    entries = ss_feed.fetch_ss_rss_feed(SS_RSS_URL)
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
    unprocessed = session.query(Entry).filter_by(is_processed=False).all()
    match_count = 0
    for entry in unprocessed:
        try:
            soup = web_utils.fetch_and_parse(entry.link)
            is_match, data = listing_analyzer.analyze_listing(soup)
            entry.is_match = is_match
            entry.is_processed = True
            entry.location = data.get('location')
            entry.building_type = data.get('building_type')
            entry.rooms = data.get('rooms')
            entry.floor = data.get('floor')
            entry.area = data.get('area')
            entry.price = data.get('price')
            entry.price_m2 = data.get('price_m2')
            if is_match:
                title = generate_title(data)
                notifier.notify_ntfy(title, entry.link)
                match_count += 1
        except Exception:
            pass
    session.commit()
    session.close()
    print(f"New entries added: {new_count}")
    print(f"Matches found: {match_count}")