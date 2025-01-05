# common/utils/timezone.py
from django.utils import timezone as dj_timezone

def now():
    """Returns the current time in IST."""
    return dj_timezone.localtime(dj_timezone.now())

def localtime(value=None):
    """Converts a datetime to local time in IST."""
    return dj_timezone.localtime(value)

def make_aware(value):
    """Converts a naive datetime to an aware datetime in IST."""
    return dj_timezone.make_aware(value, dj_timezone.get_current_timezone())

def make_naive(value):
    """Converts an aware datetime to a naive datetime in IST."""
    return dj_timezone.make_naive(value, dj_timezone.get_current_timezone())

def is_aware(value):
    """Checks if a datetime is timezone-aware."""
    return dj_timezone.is_aware(value)

def is_naive(value):
    """Checks if a datetime is naive."""
    return dj_timezone.is_naive(value)
