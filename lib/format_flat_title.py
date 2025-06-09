# file format_flat_title.py
# tihs function formats the title of a flat listing

def format_flat_title(location, region, street):
    parts = []
    if location:
        parts.append(location)
    if region and region != location:
        parts.append(region)
    if street:
        parts.append(street)
    return ', '.join(parts)
