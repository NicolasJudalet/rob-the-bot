"""
Tests the should_send_reminder_today helper
"""
import datetime

from django.test import TestCase
from unittest.mock import patch

from hello.helpers.should_send_reminder_today import should_send_reminder_today


class MockDate(datetime.date):
    @classmethod
    def weekday(cls):
        return 0


class ShouldSendReminderTodayTest(TestCase):
    """
    Test should_send_reminder_today helper
    """

    @patch("hello.helpers.should_send_reminder_today.settings")
    @patch("hello.helpers.should_send_reminder_today.datetime")
    @patch("hello.helpers.should_send_reminder_today.get_weekdays")
    def test_should_send_reminder_today_should_return_true(
        self, get_weekdays, datetime, settings
    ):
        datetime.datetime.today.return_value = MockDate(2020, 8, 26)
        settings.SEND_REMINDER_WEEKDAYS = [
            "Tuesday",
            "Friday",
        ]
        get_weekdays.return_value = ["Tuesday"]

        self.assertEqual(should_send_reminder_today(), True)

    @patch("hello.helpers.should_send_reminder_today.settings")
    @patch("hello.helpers.should_send_reminder_today.datetime")
    @patch("hello.helpers.should_send_reminder_today.get_weekdays")
    def test_should_send_reminder_today_should_return_false(
        self, get_weekdays, datetime, settings
    ):
        datetime.datetime.today.return_value = MockDate(2020, 8, 26)
        settings.SEND_REMINDER_WEEKDAYS = [
            "Wednesday",
            "Friday",
        ]
        get_weekdays.return_value = ["Tuesday"]

        self.assertEqual(should_send_reminder_today(), False)
