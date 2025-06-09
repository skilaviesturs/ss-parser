from telegram import Update
from telegram.ext import ContextTypes
from lib.db_utils import Session, MonitoredFlat
from lib.logger import logger
from lib.format_flat_title import format_flat_title

async def handle_unmonitor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    entry_hash = query.data.split(":", 1)[1]

    with Session() as session:
        try:
            flat = session.query(MonitoredFlat).filter_by(hash=entry_hash).first()
            if flat:
                title = format_flat_title(flat.location, flat.region, flat.street)
                session.delete(flat)
                session.commit()
                await query.edit_message_text(
                    text=f"<b>{title}</b>\n❌ monitorings atcelts",
                    parse_mode="HTML"
                )
            else:
                await query.edit_message_text("⚠️ Dzīvoklis netiek monitorēts vai netika atrasts.")
        except Exception as e:
            logger.error(f"[monitor] ❌ Neizdevās dzēst no monitoringa: {e}")
            await query.edit_message_text("❌ Kļūda atceļot monitoringu.")
