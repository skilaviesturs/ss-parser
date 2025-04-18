import requests
import config

def notify_ntfy(title, link):
    url = config.NTFY_URL.rstrip('/')
    topic = 'ss-matches'
    full_url = f"{url}/{topic}"
    message = f"{title}\n{link}"
    auth = (config.NTFY_USERNAME, config.NTFY_PASSWORD) if config.NTFY_USERNAME and config.NTFY_PASSWORD else None
    headers = {'Title': title}
    response = requests.post(full_url, data=message.encode('utf-8'), headers=headers, auth=auth)
    response.raise_for_status()
    return response.status_code
