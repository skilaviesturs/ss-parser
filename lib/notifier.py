# file notifier.py
# This module provides functions to send notifications via NTFY and/or Telegram.
import requests
import lib.config as config
from lib.notifier_telegram import notify_telegram
from lib.logger import logger


async def notify(title: str, body: str, entry_hash: str = None) -> bool:
    sent = False

    if config.NTFY_URL:
        try:
            sent |= notify_ntfy(title, body)
        except Exception as e:
            logger.warning(f"[notify] ❌ NTFY failed: {e}")

    if config.TELEGRAM_CHAT_ID:
        try:
            sent |= await notify_telegram(title, body, entry_hash)
        except Exception as e:
            logger.warning(f"[notify] ❌ Telegram failed: {e}")

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

