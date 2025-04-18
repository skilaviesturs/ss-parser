import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def get_list_from_env(var_name):
    value = os.getenv(var_name, '')
    if value.strip() == '':
        return []
    return [v.strip() for v in value.split(',') if v.strip()]

SS_RSS_URL = os.getenv('SS_RSS_URL', '')
LOCATION = get_list_from_env('LOCATION')
BUILDING_TYPE = get_list_from_env('BUILDING_TYPE')
ROOMS = os.getenv('ROOMS', '')
FLOOR = os.getenv('FLOOR', '')
AREA = os.getenv('AREA', '')
PRICE = os.getenv('PRICE', '')
PROPERTIES = get_list_from_env('PROPERTIES')
NTFY_URL = os.getenv('NTFY_URL', '')
NTFY_USERNAME = os.getenv('NTFY_USERNAME', '')
NTFY_PASSWORD = os.getenv('NTFY_PASSWORD', '')
