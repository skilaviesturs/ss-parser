import ss_feed
from db_utils import save_entries_to_db, Session, Entry
from config import SS_RSS_URLS
import web_utils
import listing_analyzer
from notifier import notify, generate_message
from logger import logger

def run_parser():
    session = Session()
    new_count = 0

    for rss_url in SS_RSS_URLS:
        entries = ss_feed.fetch_ss_rss_feed(rss_url)
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
            entry.region = data.get('region')
            entry.building_type = data.get('building_type')
            entry.rooms = data.get('rooms')
            entry.floor = data.get('floor')
            entry.area = data.get('area')
            entry.price = data.get('price')
            entry.price_m2 = data.get('price_m2')
            entry.street = data.get('street')
            if is_match:
                title, body = generate_message(data, entry.link)
                # logger.info(f">>> DEBUG DATA DUMP: region={data['region']}, location={data['location']}")
                logger.info(f"[parser] MATCH:\n{title}\nMESSAGE: {body}")
                notify(title, body)
                match_count += 1
        except Exception:
            pass

    session.commit()
    session.close()
    logger.info(f"[parser] New entries added: {new_count}")
    logger.info(f"[parser] Matches found: {match_count}")