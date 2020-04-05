"""
Tests for the message type repository
"""
import os

from unittest.mock import patch
from django.test import TestCase

from hello.models.message_type import MessageType
from hello.repositories.message_type import get_hydrated_message_body


class TestSlackUserRepository(TestCase):
    def setUp(self):
        MessageType.objects.create(
            name="skill_form_reminder_v1",
            template_file="reminder_message_payload.json",
        )
        MessageType.objects.create(
            name="skill_form_reminder_v2",
            template_file="reminder_message_payload_v2.json",
        )

    @patch(
        "hello.repositories.message_type.json.dumps",
        return_value='{"url":"___skill_form_url___", "icon":"___form_icon_url___"}',
    )
    def test_get_hydrated_message_body(self, json_dumps):
        """
        Tests that get_hydrated_message_body correctly replaces the placeholders in message body
        """
        self.assertEqual(
            get_hydrated_message_body(1),
            '{{"url":"{}", "icon":"{}"}}'.format(
                os.environ.get("SKILL_FORM_URL"), os.environ.get("FORM_ICON_URL"),
            ),
        )
        self.assertEqual(
            get_hydrated_message_body(2),
            '{{"url":"{}", "icon":"{}"}}'.format(
                os.environ.get("SKILL_FORM_V2_URL"), os.environ.get("FORM_ICON_URL"),
            ),
        )
