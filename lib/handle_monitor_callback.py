from telegram import Update
from telegram.ext import ContextTypes
from lib.db_utils import Session, Entry, MonitoredFlat
from lib.logger import logger
from lib.format_flat_title import format_flat_title

async def handle_monitor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    entry_hash = query.data.split(":", 1)[1]

    with Session() as session:
      try:
          exists = session.query(MonitoredFlat).filter_by(hash=entry_hash).first()
          if exists:
              title = format_flat_title(exists.location, exists.region, exists.street)
              message = f"<b>{title}</b>\n❗ jau tiek monitorēts."
              await query.message.reply_text(message, parse_mode="HTML")
          else:
              entry = session.query(Entry).filter_by(hash=entry_hash).first()
              if not entry:
                  await query.message.reply_text("❌ Dzīvokļa dati nav atrasti.")
                  await query.edit_message_reply_markup(reply_markup=None)
                  return

              monitored = MonitoredFlat(
                  hash=entry.hash,
                  location=entry.location,
                  region=entry.region,
                  street=entry.street,
                  building_type=entry.building_type,
                  rooms=entry.rooms,
                  floor=entry.floor,
                  area=entry.area,
                  link=entry.link,
                  price=entry.price,
              )
              session.add(monitored)
              session.commit()

              title = format_flat_title(entry.location, entry.region, entry.street)
              message = f"<b>{title}</b>\n✅ pievienots monitoringam."
              await query.message.reply_text(message, parse_mode="HTML")
      except Exception as e:
          logger.info(f"[monitor] ❌ Kļūda saglabājot monitorēšanu: {e}")
          await query.message.reply_text("❌ Neizdevās pievienot monitorēšanai.")