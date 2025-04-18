import config

SEARCH_LOCATION = config.LOCATION
SEARCH_BUILDING_TYPE = config.BUILDING_TYPE
SEARCH_ROOMS = config.ROOMS
SEARCH_FLOOR = config.FLOOR
SEARCH_AREA = config.AREA
SEARCH_PRICE = config.PRICE
SEARCH_PROPERTIES = config.PROPERTIES


def extract_listing_data(soup):
    """
    Extracts relevant fields from a parsed listing BeautifulSoup object.
    Returns a dict with keys: location, building_type, rooms, floor, area, price, text.
    """
    data = {
        'location': None,
        'building_type': None,
        'rooms': None,
        'floor': None,
        'area': None,
        'price': None,
        'text': soup.get_text(separator=' ', strip=True)
    }
    # Example extraction logic (update selectors as needed for ss.lv)
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 2:
            continue
        label = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)
        if 'Rajons' in label:
            data['location'] = value
        elif 'Mājas tips' in label:
            data['building_type'] = value
        elif 'Istabas' in label:
            try:
                data['rooms'] = int(value)
            except Exception:
                pass
        elif 'Stāvs' in label:
            try:
                floor_val = value.split('/')[0].strip()
                data['floor'] = int(floor_val)
            except Exception:
                pass
        elif 'Platība' in label:
            try:
                data['area'] = float(value.split()[0].replace(',', '.'))
            except Exception:
                pass
        elif 'Cena' in label:
            try:
                data['price'] = float(value.split()[0].replace(',', '').replace('€', ''))
            except Exception:
                pass
    return data


def matches_search_criteria(data):
    """
    Returns True if the listing data matches the search criteria from config.
    """
    if SEARCH_LOCATION and data['location'] not in SEARCH_LOCATION:
        return False
    if SEARCH_BUILDING_TYPE and data['building_type'] not in SEARCH_BUILDING_TYPE:
        return False
    if SEARCH_ROOMS and (data['rooms'] is None or data['rooms'] < int(SEARCH_ROOMS[0])):
        return False
    if SEARCH_FLOOR and (data['floor'] is None or data['floor'] < int(SEARCH_FLOOR[0])):
        return False
    if SEARCH_AREA and (data['area'] is None or data['area'] < float(SEARCH_AREA[0])):
        return False
    if SEARCH_PRICE and (data['price'] is None or data['price'] > float(SEARCH_PRICE[0])):
        return False
    if SEARCH_PROPERTIES:
        found = False
        for prop in SEARCH_PROPERTIES:
            if prop.lower() in data['text'].lower():
                found = True
                break
        if not found:
            return False
    return True


def analyze_listing(soup):
    """
    Analyze a parsed listing soup and return True if it matches search criteria.
    """
    data = extract_listing_data(soup)
    return matches_search_criteria(data)
