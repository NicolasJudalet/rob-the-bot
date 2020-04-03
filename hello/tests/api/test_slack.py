"""
Tests for the api submodule
"""
import os

from unittest.mock import patch, call

from django.test import TestCase

from hello.api import send_reminder
from hello.models import SlackUser


class TestSlack(TestCase):
    def setUp(self):
        self.user_1 = SlackUser.objects.create(
            slack_id = "user_id_1",
            channel_id = "channel_id_1",
            has_answered_skill_form = False,
        )
        self.user_2 = SlackUser.objects.create(
            slack_id = "user_id_2",
            channel_id = "channel_id_2",
            has_answered_skill_form = True,
        )

    @patch(
        "hello.api.slack.os.environ.get",
        side_effect=["skill_form_url", "form_icon_url"] + ["slack_url", "slack_token"] * 2,
    )
    @patch("hello.api.slack.requests.post")
    def test_send_reminder(self, post, get):
        send_reminder([self.user_1, self.user_2])

        post.assert_has_calls([
            call(
                "slack_url/chat.postMessage",
                data="{\"channel\": \"channel_id_1\", \"blocks\": [{\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"Hello !\\n\\nPour te trouver la meilleure mission possible, *nous avons besoin que tu remplisses le formulaire suivant.*\\n\\nCela ne te prendra pas plus de 5 min et \\u00e7a nous aidera \\u00e0 mieux conna\\u00eetre tes comp\\u00e9tences et tes envies !\"}}, {\"type\": \"divider\"}, {\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"<skill_form_url|*Pour mieux te conna\\u00eetre*>\\nGoogle Form\\nDur\\u00e9e : 5 min\"}, \"accessory\": {\"type\": \"image\", \"image_url\": \"form_icon_url\", \"alt_text\": \"Google Form\"}}, {\"type\": \"divider\"}, {\"type\": \"actions\", \"elements\": [{\"type\": \"button\", \"text\": {\"type\": \"plain_text\", \"emoji\": true, \"text\": \"Ok, c\'est fait !\"}, \"style\": \"primary\", \"value\": \"form_filled\"}, {\"type\": \"button\", \"text\": {\"type\": \"plain_text\", \"emoji\": true, \"text\": \"Rappelle le moi demain\"}, \"style\": \"danger\", \"value\": \"form_not_filled\"}]}]}",
                headers={"Authorization": "Bearer slack_token", "Content-type": "application/json"}
            ),
            call(
                "slack_url/chat.postMessage",
                data="{\"channel\": \"channel_id_2\", \"blocks\": [{\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"Hello !\\n\\nPour te trouver la meilleure mission possible, *nous avons besoin que tu remplisses le formulaire suivant.*\\n\\nCela ne te prendra pas plus de 5 min et \\u00e7a nous aidera \\u00e0 mieux conna\\u00eetre tes comp\\u00e9tences et tes envies !\"}}, {\"type\": \"divider\"}, {\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"<skill_form_url|*Pour mieux te conna\\u00eetre*>\\nGoogle Form\\nDur\\u00e9e : 5 min\"}, \"accessory\": {\"type\": \"image\", \"image_url\": \"form_icon_url\", \"alt_text\": \"Google Form\"}}, {\"type\": \"divider\"}, {\"type\": \"actions\", \"elements\": [{\"type\": \"button\", \"text\": {\"type\": \"plain_text\", \"emoji\": true, \"text\": \"Ok, c\'est fait !\"}, \"style\": \"primary\", \"value\": \"form_filled\"}, {\"type\": \"button\", \"text\": {\"type\": \"plain_text\", \"emoji\": true, \"text\": \"Rappelle le moi demain\"}, \"style\": \"danger\", \"value\": \"form_not_filled\"}]}]}",
                headers={"Authorization": "Bearer slack_token", "Content-type": "application/json"}
            )
        ])
