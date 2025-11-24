"""
Validation utilities for input sanitization and validation.
"""
from flask import current_app
from datetime import datetime
from typing import Optional
import re


def validate_file_type(filename: str) -> bool:
    """
    Validate file extension is allowed.
    
    Args:
        filename: Name of the file
    
    Returns:
        True if file type is allowed, False otherwise
    """
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def validate_file_size(file_size: int) -> bool:
    """
    Validate file size is within limits.
    
    Args:
        file_size: Size of file in bytes
    
    Returns:
        True if file size is valid, False otherwise
    """
    max_size = current_app.config['MAX_FILE_SIZE']
    return file_size <= max_size


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Optional maximum length
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Trim whitespace
    text = text.strip()
    
    # Apply length limit if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def parse_datetime(date_str: str, time_str: Optional[str] = None) -> Optional[datetime]:
    """
    Parse date and time strings into datetime object.
    
    Args:
        date_str: Date string in format 'YYYY-MM-DD'
        time_str: Optional time string in format 'HH:MM:SS'
    
    Returns:
        Datetime object or None if parsing fails
    """
    try:
        if time_str:
            datetime_str = f"{date_str} {time_str}"
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        else:
            return datetime.strptime(date_str, '%Y-%m-%d')
    except (ValueError, TypeError):
        return None


def validate_datetime_format(datetime_str: str) -> bool:
    """
    Validate datetime string format.
    
    Args:
        datetime_str: Datetime string to validate
    
    Returns:
        True if format is valid, False otherwise
    """
    try:
        datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return True
    except (ValueError, TypeError):
        return False


def validate_date_format(date_str: str) -> bool:
    """
    Validate date string format.
    
    Args:
        date_str: Date string to validate
    
    Returns:
        True if format is valid, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


