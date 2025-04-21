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
    # Default to a file in the data directory
    return 'sqlite:///data/ss_entries.db'

# Ensure the URL does not have extra quotes
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
