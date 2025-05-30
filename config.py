import os
from dotenv import load_dotenv

load_dotenv()

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

SS_RSS_URL = os.getenv('SS_RSS_URL', '').strip('"')
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

