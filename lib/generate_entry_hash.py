# file: generate_entry_hash.py
# This module provides a function to generate a unique hash for a real estate entry.
import hashlib
def generate_entry_hash(data: dict) -> str:
    raw = f"{data['location']}|{data['region']}|{data['street']}|{data['building_type']}|{data['rooms']}|{data['floor']}|{data['area']}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

