import lib.ss_feed as ss_feed
from lib.db_utils import Session, Entry, FlatPriceHistory
from lib.config import SS_RSS_URLS
import lib.web_utils as web_utils
import lib.listing_analyzer as listing_analyzer
from lib.logger import logger
from datetime import date
from lib.generate_entry_hash import generate_entry_hash
from lib.generate_message import generate_message
from lib.notifier import notify

today = date.today()

async def run_parser():
    new_count = 0
    match_count = 0

    with Session() as session:

      for rss_url in SS_RSS_URLS:
          entries = ss_feed.fetch_ss_rss_feed(rss_url)
          for entry in entries:
              link = entry.get('link')

              exists = session.query(Entry).filter_by(link=link).first()
              if not exists:
                  db_entry = Entry(
                      title=entry.get('title'),
                      link=link,
                      published=entry.get('published'),
                      is_processed=False,
                      date_published=today,
                  )
                  session.add(db_entry)
                  new_count += 1

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
                  entry_hash = generate_entry_hash(data)

                  existing_entry = session.query(Entry).filter_by(hash=entry_hash).first()
                  title, body = generate_message(data, entry.link)

                  should_notify = False

                  if existing_entry:
                      logger.debug(f"[parser] ⚠️ Dzīvoklis jau eksistē ar hash {entry_hash}.")
                      price_changed = existing_entry.price != data.get('price')
                      link_changed = existing_entry.link != entry.link

                      if price_changed or link_changed:
                          logger.debug(f"[parser] 🔁 Cena vai links mainījies — sūtam notifikāciju.")

                          price_log = FlatPriceHistory(
                              hash=entry_hash,
                              date=today,
                              price=data.get('price')
                          )
                          session.add(price_log)

                          should_notify = True
                      else:
                          logger.debug(f"[parser] ⏩ Nav izmaiņu — izlaižam notifikāciju.")

                      # Atjaunojam esošo ierakstu vienmēr
                      existing_entry.link = entry.link
                      existing_entry.price = data.get('price')
                      existing_entry.price_m2 = data.get('price_m2')
                      existing_entry.published = entry.published
                      existing_entry.date_published = today
                      existing_entry.is_processed = True
                      existing_entry.is_match = True

                  else:
                      # Jauns ieraksts
                      logger.debug(f"[parser] 🆕 Jauns dzīvoklis ar hash {entry_hash}")
                      entry.hash = entry_hash
                      should_notify = True

                  if should_notify:
                      logger.debug(f">>> DEBUG DATA DUMP: region={data['region']}, location={data['location']}")
                      logger.info(f"[parser] →\nMATCH: {title}\nMESSAGE: {body}")
                      await notify(title, body, entry_hash=entry_hash)
                      match_count += 1

          except Exception as e:
              logger.info(f"[parser] Failed to process {entry.link}: {str(e)}")

      session.commit()
    
    logger.info(f"[parser] New entries added from RSS feed: {new_count}")
    logger.info(f"[parser] Matches found: {match_count}")