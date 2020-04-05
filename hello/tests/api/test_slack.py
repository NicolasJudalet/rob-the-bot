"""
Tests for the api submodule
"""
from unittest.mock import patch, call

from django.test import TestCase

from hello.api.slack import send_message
from hello.models.slack_user import SlackUser


class TestSlack(TestCase):
    def setUp(self):
        self.user_1 = SlackUser.objects.create(
            slack_id="user_id_1", channel_id="channel_id_1",
        )

    @patch("hello.api.slack.os.environ.get", side_effect=["slack_url", "slack_token"])
    @patch("hello.api.slack.requests.post")
    def test_send_message(self, post, get):
        message_body = '{"channel_id":"___channel_id___"}'
        send_message(message_body, self.user_1)

        post.assert_called_with(
            "slack_url/chat.postMessage",
            data='{"channel_id":"channel_id_1"}',
            headers={
                "Authorization": "Bearer slack_token",
                "Content-type": "application/json",
            },
        )
