import requests
import config
import urllib.parse
from telegram import Bot
import asyncio

# Inicializē Telegram botu, ja TOKEN ir pieejams
telegram_bot = Bot(token=config.TELEGRAM_TOKEN) if config.TELEGRAM_TOKEN else None

# Izveido vai iegūst esošo event loop (lai izvairītos no RuntimeError)
try:
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

def notify(title, link):
    sent = False

    if config.NTFY_URL:
        sent |= notify_ntfy(title, link)

    if telegram_bot and config.TELEGRAM_CHAT_ID:
        sent |= notify_telegram(title, link)

    if not sent:
        print("[notify] ⚠️ No notification method configured!")

    return sent

def notify_ntfy(title, link):
    try:
        url = config.NTFY_URL.rstrip('/')
        topic = 'ss-matches'
        full_url = f"{url}/{topic}"
        message = f"{title}\n{link}"
        auth = (config.NTFY_USERNAME, config.NTFY_PASSWORD) if config.NTFY_USERNAME and config.NTFY_PASSWORD else None
        headers = {}
        response = requests.post(full_url, data=message.encode('utf-8'), headers=headers, auth=auth)
        response.raise_for_status()
        print(f"[notify_ntfy] ✅ Sent to ntfy")
        return True
    except Exception as e:
        print(f"[notify_ntfy] ❌ Failed: {e}")
        return False

def notify_telegram(title, link):
    if not telegram_bot or not config.TELEGRAM_CHAT_ID:
        return False
    try:
        location, street, rest = split_title(title)
        message = f"<b>{location}, {street}</b>\n{rest}\n{link}"
        loop.run_until_complete(
            telegram_bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode="HTML"
            )
        )
        print(f"[notify_telegram] ✅ Sent to Telegram")
        return True
    except Exception as e:
        print(f"[notify_telegram] ❌ Failed: {e}")
        return False

def split_title(full_title: str):
    """
    Sadala pilno title daļu trīs komponentēs:
    - location
    - street
    - pārējie dati
    """
    parts = full_title.split(', ')
    location = parts[0] if len(parts) > 0 else ''
    street = parts[1] if len(parts) > 1 else ''
    rest = ', '.join(parts[2:]) if len(parts) > 2 else ''
    return location, street, rest

def generate_title(data):
    parts = filter(None, [
        data.get('location'),
        data.get('street'),
        f"{data['building_type']}" if data.get('building_type') else None,
        f"{data['rooms']} istaba" if data['rooms'] == 1 else f"{data['rooms']} istabas" if data.get('rooms') else None,
        f"{data['floor']} stāvs" if data.get('floor') else None,
        f"{data['area']} m²" if data.get('area') else None,
        f"{data['price']} €" if data.get('price') else None,
        f"({data['price_m2']} €/m²)" if data.get('price_m2') else None,
    ])
    return ', '.join(parts)
