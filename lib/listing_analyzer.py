import lib.config as config
from lib.logger import logger

def extract_listing_data(soup):
    data = {
        'location': None,
        'region': None,
        'building_type': None,
        'rooms': None,
        'floor': None,
        'area': None,
        'price': None,
        'street': None,
        'price_m2': None,
        'text': soup.get_text(separator=' ', strip=True)
    }

    LABELS = config.LABELS
    location = None
    region = None

    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 2:
            continue
        label = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True).replace('[Karte]', '').strip()

        if any(lab in label for lab in LABELS['location']):
            location = value

        elif any(lab in label for lab in LABELS['region']):
            region = value

        elif any(lab in label for lab in LABELS['street']):
            data['street'] = value

        elif any(lab in label for lab in LABELS['building_type']):
            data['building_type'] = value

        elif any(lab in label for lab in LABELS['rooms']):
            try:
                data['rooms'] = int(value)
            except Exception:
                pass

        elif any(lab in label for lab in LABELS['floor']):
            try:
                data['floor'] = int(value.split('/')[0].strip())
            except Exception:
                pass

        elif any(lab in label for lab in LABELS['area']):
            try:
                data['area'] = float(value.split()[0].replace(',', '.'))
            except Exception:
                pass

        elif any(lab in label for lab in LABELS['price']):
            try:
                import re
                price_match = re.search(r'([\d\s]+)\s*€', value)
                price_m2_match = re.search(r'\(([^€]+)€/m²\)', value)
                if price_match:
                    price_str = price_match.group(1).replace(' ', '').replace(',', '')
                    data['price'] = int(float(price_str))
                if price_m2_match:
                    price_m2_str = price_m2_match.group(1).replace(' ', '').replace(',', '.')
                    data['price_m2'] = float(price_m2_str)
            except Exception:
                pass

    data['region'] = region
    data['location'] = location

    return data


def matches_search_criteria(data):
    # LOCATION match: pārbauda gan 'location', gan 'region'
    if config.LOCATION:
      location_match = False
      loc_field = (data.get('location') or '').lower()
      region_field = (data.get('region') or '').lower()

    for loc in config.LOCATION:
        loc = loc.lower().strip()

        if config.STRICT_LOCATION_MATCH:
            if loc == loc_field or loc == region_field:
                location_match = True
                break
        else:
            if loc in loc_field or loc in region_field:
                location_match = True
                break

    if not location_match:
        logger.debug(f"❌ Rejected by LOCATION: '{data.get('location')}' / '{data.get('region')}' vs {config.LOCATION}")
        return False

    if config.BUILDING_TYPE and data['building_type'] not in config.BUILDING_TYPE:
        logger.debug(f"❌ Rejected by BUILDING_TYPE: '{data['building_type']}'")
        return False

    if config.ROOMS and (data['rooms'] is None or data['rooms'] < config.ROOMS):
        logger.debug(f"❌ Rejected by ROOMS: '{data['rooms']}' < {config.ROOMS}")
        return False

    if config.FLOOR and (data['floor'] is None or data['floor'] < config.FLOOR):
        logger.debug(f"[DEBUG] ❌ Rejected by FLOOR: '{data['floor']}' < {config.FLOOR}")
        return False

    if config.AREA and (data['area'] is None or data['area'] < config.AREA):
        logger.debug(f"❌ Rejected by AREA: '{data['area']}' < {config.AREA}")
        return False

    if config.PRICE and (data['price'] is None or data['price'] > config.PRICE):
        logger.debug(f"❌ Rejected by PRICE: '{data['price']}' > {config.PRICE}")
        return False

    if config.PROPERTIES:
        text_lower = data['text'].lower() if data['text'] else ''
        if not any(prop.lower() in text_lower for prop in config.PROPERTIES):
            logger.debug(f"❌ Rejected by PROPERTIES: text doesn't include any of {config.PROPERTIES}")
            return False

    logger.debug(f"✅ MATCH OK: '{data.get('location')}'")
    return True


def analyze_listing(soup):
    data = extract_listing_data(soup)
    logger.debug(f"Extracted location: {data.get('location')}")
    is_match = matches_search_criteria(data)
    return is_match, data
