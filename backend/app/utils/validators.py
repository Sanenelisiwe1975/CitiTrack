"""Input validators"""
import re
from typing import Tuple


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """Validate South African phone number"""
    
    # Remove spaces and dashes
    phone = phone.replace(' ', '').replace('-', '')
    
    # South African phone patterns
    patterns = [
        r'^\+27\d{9}$',  # +27XXXXXXXXX
        r'^27\d{9}$',    # 27XXXXXXXXX
        r'^0\d{9}$',     # 0XXXXXXXXX
    ]
    
    for pattern in patterns:
        if re.match(pattern, phone):
            # Normalize to +27 format
            if phone.startswith('0'):
                phone = '+27' + phone[1:]
            elif phone.startswith('27'):
                phone = '+' + phone
            return True, phone
    
    return False, "Invalid phone number format"


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """Validate coordinates are within South Africa"""
    
    # South Africa approximate bounds
    # Latitude: -35 to -22
    # Longitude: 16 to 33
    
    if not (-35 <= latitude <= -22):
        return False, "Latitude outside South Africa"
    
    if not (16 <= longitude <= 33):
        return False, "Longitude outside South Africa"
    
    return True, "Valid coordinates"


def sanitize_text(text: str, max_length: int = 1000) -> str:
    """Sanitize user input text"""
    
    # Remove potential HTML/script tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Trim to max length
    text = text[:max_length]
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text.strip()