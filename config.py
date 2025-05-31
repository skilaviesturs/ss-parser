import os
from dotenv import load_dotenv

def is_running_in_docker():
    # Nosaka, vai Python darbojas Docker konteinerī
    try:
        if os.path.exists('/.dockerenv'):
            return True
        with open('/proc/1/cgroup', 'rt') as f:
            return 'docker' in f.read() or 'kubepods' in f.read()
    except Exception:
        return False

# Tikai ārpus Docker ielādē .env failu
if not is_running_in_docker():
    load_dotenv()

def get_list_from_env(var_name):
    value = os.getenv(var_name, '')
    if value.strip() == '':
        return []
    return [v.strip() for v in value.split(';') if v.strip()]

def get_int_from_env(var_name, default=0):
    try:
        return int(os.getenv(var_name, default))
    except ValueError:
        return default

def get_database_path():
    db_path = os.getenv('DATABASE_PATH', 'sqlite:///data/ss_entries.db')
    return db_path

def get_all_rss_urls():
    urls = []
    index = 1
    while True:
        key = f'SS_RSS_URL_{index}'
        url = os.getenv(key)
        if not url:
            break
        urls.append(url.strip())
        index += 1
    return urls

SS_RSS_URLS = get_all_rss_urls()

LOCATION = get_list_from_env('LOCATION')
BUILDING_TYPE = get_list_from_env('BUILDING_TYPE')
ROOMS = get_int_from_env('ROOMS')
FLOOR = get_int_from_env('FLOOR')
AREA = get_int_from_env('AREA')
PRICE = get_int_from_env('PRICE')
PROPERTIES = get_list_from_env('PROPERTIES')
NTFY_URL = os.getenv('NTFY_URL', '')
NTFY_USERNAME = os.getenv('NTFY_USERNAME', '')
NTFY_PASSWORD = os.getenv('NTFY_PASSWORD', '')
DATABASE_PATH = get_database_path()
PARSE_INTERVAL_MINUTES = get_int_from_env('PARSE_INTERVAL_MINUTES', 30)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def get_label_list(var_name, default=''):
    val = os.getenv(var_name, default)
    return [v.strip() for v in val.split(';') if v.strip()]

LABELS = {
    'location': get_label_list('LABEL_LOCATION', 'Pilsēta/pagasts'),
    'street': get_label_list('LABEL_STREET', 'Iela'),
    'building_type': get_label_list('LABEL_BUILDING_TYPE', 'Sērija'),
    'rooms': get_label_list('LABEL_ROOMS', 'Istabas'),
    'floor': get_label_list('LABEL_FLOOR', 'Stāvs'),
    'area': get_label_list('LABEL_AREA', 'Platība'),
    'price': get_label_list('LABEL_PRICE', 'Cena'),
}