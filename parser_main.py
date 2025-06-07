import ss_feed
from db_utils import save_entries_to_db, Session, Entry
from config import SS_RSS_URLS
import web_utils
import listing_analyzer
from notifier import notify, generate_message
from logger import logger
from datetime import date

today = date.today()

def run_parser():
    new_count = 0
    match_count = 0
    # Obligāti jāievāc visi šodienas RSS feed linki, lai saprastu, kas pazudis
    all_current_links = set()

    with Session() as session:

      for rss_url in SS_RSS_URLS:
          entries = ss_feed.fetch_ss_rss_feed(rss_url)
          for entry in entries:
              link = entry.get('link')  # ← Saglabājam link mainīgajā
              all_current_links.add(link)  # ✅ Reģistrējam kā "šodien redzētu" sludinājumu

              exists = session.query(Entry).filter_by(link=link).first()
              if not exists:
                  db_entry = Entry(
                      title=entry.get('title'),
                      link=link,
                      published=entry.get('published'),
                      is_processed=False,
                      date_published=today,  # ✅ jauns ieraksts
                      date_removed=None      # vēl nav beidzies
                  )
                  session.add(db_entry)
                  new_count += 1
              else:
                # ✅ Ja ieraksts parādās atkal, bet iepriekš bija noņemts — notīri date_removed
                if exists.date_removed is not None:
                  exists.date_removed = None

      session.commit()

      unprocessed = session.query(Entry).filter_by(is_processed=False).all()
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
                  logger.debug(f">>> DEBUG DATA DUMP: region={data['region']}, location={data['location']}")
                  logger.info(f"[parser] →\nMATCH: {title}\nMESSAGE: {body}")
                  notify(title, body)
                  match_count += 1
          except Exception as e:
              logger.info(f"[parser] Failed to process {entry.link}: {str(e)}")

      # ✅ Atrodam sludinājumus, kas vairs nav feedā – ieliekam date_removed
      active_entries = session.query(Entry).filter(Entry.date_removed == None).all()
      for entry in active_entries:
          if entry.link not in all_current_links:
              entry.date_removed = today
              logger.info(f"[parser] Marked as removed: {entry.link}")

      session.commit()

      removed_today = session.query(Entry).filter(Entry.date_removed == today).count()
    
    # Logs ārpus `with`, sesija šeit jau ir aizvērta
    logger.info(f"[parser] New entries added from RSS feed: {new_count}")
    logger.info(f"[parser] Matches found: {match_count}")
    logger.info(f"[parser] Entries removed from RSS feed today: {removed_today}")