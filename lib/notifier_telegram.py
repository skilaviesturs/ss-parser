from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application
import lib.config as config
from lib.logger import logger

# Telegram app un bot — jāinicializē main.py failā un jāpārnes šurp caur import
telegram_bot: Bot = None
telegram_app: Application = None

def set_telegram_context(bot: Bot, app: Application):
    global telegram_bot, telegram_app
    telegram_bot = bot
    telegram_app = app

async def notify_telegram(title: str, body: str, entry_hash: str = None):
    if not telegram_bot or not config.TELEGRAM_CHAT_ID or not telegram_app:
        return False
    try:
        message = f"<b>{title}</b>\n{body}"

        reply_markup = None
        if entry_hash:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("📍 Monitorēt šo dzīvokli", callback_data=f"monitor:{entry_hash}")]
            ])

        telegram_app.create_task(
            telegram_bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        )
        logger.info(f"[tele] ✅ Sent to Telegram\n")
        return True
    except Exception as e:
        logger.info(f"[tele] ❌ Failed: {e}\n")
        return False


