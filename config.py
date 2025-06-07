import os
import json
import sys
from dotenv import load_dotenv
from logger import logger

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
    load_dotenv(override=True)

def get_list_from_env(var_name):
    value = os.getenv(var_name, '')
    if value.strip() == '':
        return []
    return [v.strip() for v in value.split(',') if v.strip()]

def get_int_from_env(var_name, default=0):
    try:
        return int(os.getenv(var_name, default))
    except ValueError:
        return default

def get_database_path():
    db_path = os.getenv('DATABASE_PATH', 'sqlite:///data/ss_entries.db')
    return db_path

def get_all_rss_urls():
    file_path = os.getenv("SS_RSS_URLS_FILE")
    if not file_path:
        raise ValueError("[config] Missing SS_RSS_URLS_FILE in environment")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            urls = json.load(f)
    except Exception as e:
        raise RuntimeError(f"[config] Failed to load RSS URLs from {file_path}: {e}")
    
    if not isinstance(urls, list) or not all(isinstance(u, str) for u in urls):
        raise ValueError(f"[config] Invalid format in {file_path}: expected list of strings")

    urls = [u.strip() for u in urls if u.strip()]

    if not urls:
        logger.error(f"[config] RSS URL list in {file_path} is empty. Terminating.")
        sys.exit(1)

    logger.info(f"[config] Loaded {len(urls)} RSS URLs from {file_path}:")
    for url in urls:
        logger.info(f" → {url}")

    return urls

def get_bool_from_env(var_name, default=False):
    val = os.getenv(var_name, str(default)).strip().lower()
    return val in ['1', 'true', 'yes']

SS_RSS_URLS = get_all_rss_urls()

LOCATION = get_list_from_env('LOCATION')
logger.info(f"[conf] Parsed LOCATION = {LOCATION}")
STRICT_LOCATION_MATCH = get_bool_from_env('STRICT_LOCATION_MATCH')
logger.info(f"[conf] Set strict LOCATION match = {STRICT_LOCATION_MATCH}")

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
    return [v.strip() for v in val.split(',') if v.strip()]

# Fiksētās vērtības no SS.lv tabulas kolonnām
LABELS = {
    'location': ['Pilsēta', 'Pilsēta/pagasts'],
    'region': ['Rajons', 'Pilsēta, rajons'],
    'street': ['Iela'],
    'building_type': ['Mājas tips'],
    'rooms': ['Istabas'],
    'floor': ['Stāvs'],
    'area': ['Platība'],
    'price': ['Cena'],
}
