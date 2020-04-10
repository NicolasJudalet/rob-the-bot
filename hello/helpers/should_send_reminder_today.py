"""
Helper to check the date and return a flag indicating if the reminder should be sent today
"""
import datetime
from django.conf import settings


def get_weekdays():
    return [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def should_send_reminder_today():
    """
    Returns a flag indicating if the reminder should be sent today (based on SEND_REMINDER_WEEKDAYS setting)
    """
    weekdays = get_weekdays()
    current_day_of_week = weekdays[datetime.datetime.today().weekday()]
    return current_day_of_week in settings.SEND_REMINDER_WEEKDAYS
