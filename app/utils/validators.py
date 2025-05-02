import re
from marshmallow import ValidationError
from typing import Optional

def validate_email(email: str) -> Optional[str]:
    """Validate email format"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return "Invalid email format"
    return None

def validate_phone_number(phone: str) -> Optional[str]:
    """Validate phone number format"""
    # Simple phone number validation - allows +, spaces, hyphens and numbers
    phone_regex = r'^\+?[0-9\s-]{10,20}$'
    if not re.match(phone_regex, phone):
        return "Invalid phone number format"
    return None

def validate_not_empty(value: str, field_name: str) -> Optional[str]:
    """Validate that a value is not empty"""
    if not value or not value.strip():
        return f"{field_name} cannot be empty"
    return None