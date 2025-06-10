from telegram import Update
from telegram.ext import ContextTypes

HELP_TEXT = """
🤖 <b>Pieejamās komandas</b>:

/help - Šis palīdzības logs
/list - Parāda monitorētos dzīvokļus
/start - Starta ziņa, kas parāda, ka bots ir aktīvs

📬 Ja kaut kas nestrādā — sazinies ar izstrādātāju.
"""

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="HTML")
