from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from lib.db_utils import Session, MonitoredFlat
from lib.logger import logger
from lib.format_flat_title import format_flat_title

async def handle_monitor_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with Session() as session:
        flats = session.query(MonitoredFlat).order_by(MonitoredFlat.created_at.desc()).all()

        if not flats:
            await update.message.reply_text("📭 Šobrīd nav neviena monitorējama dzīvokļa.")
            return

        for flat in flats:
            title = format_flat_title(flat.location, flat.region, flat.street)
            body_parts = [
                f"{flat.building_type}" if flat.building_type else None,
                f"{flat.rooms} istabas" if flat.rooms else None,
                f"{flat.floor}. stāvs" if flat.floor else None,
                f"{flat.area} m²" if flat.area else None,
                f"{flat.price} €" if flat.price else None
            ]
            body = ', '.join(filter(None, body_parts))
            link = f"\n<a href='{flat.link}'>✅  Skatīt sludinājumu</a>"

            msg = f"<b>{title}</b>\n{body}\n{link if link else ''}"

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌  Atteikties no monitoringa", callback_data=f"unmonitor:{flat.hash}")]
            ])

            await update.message.reply_text(
                msg,
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
