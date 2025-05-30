import config

def extract_listing_data(soup):
    data = {
        'location': None,
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

    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < 2:
            continue
        label = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)

        if any(lab in label for lab in LABELS['location']):
            data['location'] = value

        elif any(lab in label for lab in LABELS['street']):
            data['street'] = value.replace('[Karte]', '').strip()

        elif any(lab in label for lab in LABELS['building_type']):
            data['building_type'] = value

        elif any(lab in label for lab in LABELS['rooms']):
            try:
                data['rooms'] = int(value)
            except Exception:
                pass

        elif any(lab in label for lab in LABELS['floor']):
            try:
                floor_val = value.split('/')[0].strip()
                data['floor'] = int(floor_val)
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
                    try:
                        data['price_m2'] = float(price_m2_str)
                    except Exception:
                        pass
            except Exception:
                pass

    return data

def matches_search_criteria(data):
    if config.LOCATION and data['location'] not in config.LOCATION:
        return False
    if config.BUILDING_TYPE and data['building_type'] not in config.BUILDING_TYPE:
        return False
    if config.ROOMS and (data['rooms'] is None or data['rooms'] < config.ROOMS):
        return False
    if config.FLOOR and (data['floor'] is None or data['floor'] < config.FLOOR):
        return False
    if config.AREA and (data['area'] is None or data['area'] < config.AREA):
        return False
    if config.PRICE and (data['price'] is None or data['price'] > config.PRICE):
        return False
    if config.PROPERTIES:
        found = False
        text_lower = data['text'].lower() if data['text'] else ''
        for prop in config.PROPERTIES:
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
