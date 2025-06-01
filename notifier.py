import requests
import config
import asyncio
from telegram import Bot
from logger import logger

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

def notify(title: str, body: str):
    sent = False

    if config.NTFY_URL:
        sent |= notify_ntfy(title, body)

    if telegram_bot and config.TELEGRAM_CHAT_ID:
        sent |= notify_telegram(title, body)

    if not sent:
        logger.info("[notify] ⚠️ No notification method configured!")

    return sent

def notify_ntfy(title: str, body: str):
    try:
        url = config.NTFY_URL.rstrip('/')
        topic = 'ss-matches'
        full_url = f"{url}/{topic}"
        auth = (
            (config.NTFY_USERNAME, config.NTFY_PASSWORD)
            if config.NTFY_USERNAME and config.NTFY_PASSWORD
            else None
        )
        headers = {"Title": title}
        response = requests.post(full_url, data=body.encode('utf-8'), headers=headers, auth=auth)
        response.raise_for_status()
        logger.info(f"[ntfy] ✅ Sent to ntfy")
        return True
    except Exception as e:
        logger.info(f"[ntfy] ❌ Failed: {e}")
        return False

def notify_telegram(title: str, body: str):
    if not telegram_bot or not config.TELEGRAM_CHAT_ID:
        return False
    try:
        message = f"<b>{title}</b>\n{body}"
        loop.run_until_complete(
            telegram_bot.send_message(
                chat_id=config.TELEGRAM_CHAT_ID,
                text=message,
                parse_mode="HTML"
            )
        )
        logger.info(f"[tele] ✅ Sent to Telegram\n")
        return True
    except Exception as e:
        logger.info(f"[tele] ❌ Failed: {e}\n")
        return False

def generate_message(data: dict, link: str) -> tuple[str, str]:
    # Virsraksts (region + location + street)
    title_parts = []

    # Vispirms vienmēr 'location' (piemēram, Rīga)
    if data.get('location'):
        title_parts.append(data['location'])
    # Tad 'region', tikai ja tas atšķiras no location
    if data.get('region') and data['region'] != data['location']:
        title_parts.append(data['region'])
    # Beigās iela
    if data.get('street'):
        title_parts.append(data['street'])

    title = ', '.join(title_parts)

    # Ķermenis (building_type, rooms, floor, area, price, price_m2)
    body_parts = list(filter(None, [
        data.get('building_type'),
        f"{data['rooms']} istaba" if data.get('rooms') == 1 else (
            f"{data['rooms']} istabas" if data.get('rooms') else None
        ),
        f"{data['floor']}. stāvs" if data.get('floor') else None,
        f"{data['area']} m²" if data.get('area') else None,
        f"{data['price']} €" if data.get('price') else None,
        f"({data['price_m2']} €/m²)" if data.get('price_m2') else None,
    ]))

    body = ', '.join(body_parts)
    body += f"\n{link}"

    return title, body
