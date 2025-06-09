# file generate_message.py
# This module provides a function to generate a message for a real estate listing.
def generate_message(data: dict, link: str) -> tuple[str, str]:
    # Virsraksts (region + location + street)
    title_parts = []

    # Vispirms vienmēr 'location' (piemēram, Rīga)
    if data.get('location'):
        title_parts.append(data['location'])
    # Tad 'region', tikai ja tas atšķiras no location
    if data.get('region') and data['region'] != data['location']:
        title_parts.append(data['region'])
    # Beigās iela
    if data.get('street'):
        title_parts.append(data['street'])

    title = ', '.join(title_parts)

    # Ķermenis (building_type, rooms, floor, area, price, price_m2)
    body_parts = list(filter(None, [
        data.get('building_type'),
        f"{data['rooms']} istaba" if data.get('rooms') == 1 else (
            f"{data['rooms']} istabas" if data.get('rooms') else None
        ),
        f"{data['floor']}. stāvs" if data.get('floor') else None,
        f"{data['area']} m²" if data.get('area') else None,
        f"{data['price']} €" if data.get('price') else None,
        f"({data['price_m2']} €/m²)" if data.get('price_m2') else None,
    ]))

    body = ', '.join(body_parts)
    body += f"\n{link}"

    return title, body