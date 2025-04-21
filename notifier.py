import requests
import config
import urllib.parse

def notify_ntfy(title, link):
    url = config.NTFY_URL.rstrip('/')
    topic = 'ss-matches'
    full_url = f"{url}/{topic}"
    safe_title = urllib.parse.quote(title, safe='')  # Ensure title is safe for POST request
    message = f"{title}\n{link}"
    auth = (config.NTFY_USERNAME, config.NTFY_PASSWORD) if config.NTFY_USERNAME and config.NTFY_PASSWORD else None
    headers = {'Title': safe_title}
    response = requests.post(full_url, data=message.encode('utf-8'), headers=headers, auth=auth)
    response.raise_for_status()
    return response.status_code

def generate_title(data):
    title_parts = []
    if data.get('location'):
        title_parts.append(data['location'])
    if data.get('building_type'):
        title_parts.append(data['building_type'])
    if data.get('rooms'):
        title_parts.append(f"{data['rooms']} rooms")
    if data.get('floor'):
        title_parts.append(f"Floor {data['floor']}")
    if data.get('area'):
        title_parts.append(f"{data['area']} m²")
    if data.get('price'):
        title_parts.append(f"{data['price']} €")
    return ', '.join(title_parts)
