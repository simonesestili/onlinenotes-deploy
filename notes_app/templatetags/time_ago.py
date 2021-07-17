from django import template
from datetime import datetime, tzinfo
import math

register = template.Library()

@register.filter(name='time_ago')
def time_ago(value):
    last_time = value.replace(tzinfo=None)
    now_time = datetime.now().replace(tzinfo=None)
    diff = math.floor((now_time - last_time).total_seconds())

    return time_format(diff)


def time_format(seconds):
    total_days = seconds // 86400
    total_hours = seconds // 3600
    total_minutes = seconds // 60

    if total_days:
        return '1 day ago' if total_days == 1 else f'{total_days} days ago'
    if total_hours:
        return '1 hour ago' if total_hours == 1 else f'{total_hours} hours ago'
    if total_minutes:
        return '1 minute ago' if total_minutes == 1 else f'{total_minutes} minutes ago'
    return '1 second ago' if seconds <= 1 else f'{seconds} seconds ago'