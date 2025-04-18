import config

SEARCH_LOCATION = config.LOCATION
SEARCH_BUILDING_TYPE = config.BUILDING_TYPE
SEARCH_ROOMS = config.ROOMS
SEARCH_FLOOR = config.FLOOR
SEARCH_AREA = config.AREA
SEARCH_PRICE = config.PRICE
SEARCH_PROPERTIES = config.PROPERTIES


def extract_listing_data(soup):
    data = {
        'location': None,
        'building_type': None,
        'rooms': None,
        'floor': None,
        'area': None,
        'price': None,
        'text': soup.get_text(separator=' ', strip=True)
    }
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
                # Extract price and price per m2 using regex
                import re
                price_match = re.search(r'([\d\s]+)\s*€', value)
                price_m2_match = re.search(r'\(([^€]+)€/m²\)', value)
                if price_match:
                    price_str = price_match.group(1).replace(' ', '').replace(',', '')
                    data['price'] = int(float(price_str))
                if price_m2_match:
                    price_m2_str = price_m2_match.group(1).replace(' ', '').replace(',', '.')
                    try:
                        data['price_m2'] = float(price_m2_str)
                    except Exception:
                        pass
            except Exception:
                pass
    return data


def matches_search_criteria(data):
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
        text_lower = data['text'].lower() if data['text'] else ''
        for prop in SEARCH_PROPERTIES:
            if prop.lower() in text_lower:
                found = True
                break
        if not found:
            return False
    return True


def analyze_listing(soup):
    data = extract_listing_data(soup)
    is_match = matches_search_criteria(data)
    return is_match, data
