"""
Tests for the slack users repository
"""
from django.test import TestCase

from hello.models.slack_user import SlackUser
from hello.repositories.slack_user import get_users_to_remind


class TestSlackUserRepository(TestCase):
    def setUp(self):
        self.user_1 = SlackUser.objects.create(
            slack_id="slack_id_1",
            channel_id="channel_id_1",
            has_answered_skill_form=False,
            has_answered_skill_form_v2=False,
            send_no_more_messages=False,
        )
        self.user_2 = SlackUser.objects.create(
            slack_id="slack_id_1",
            channel_id="channel_id_1",
            has_answered_skill_form=False,
            has_answered_skill_form_v2=True,
            send_no_more_messages=False,
        )
        self.user_3 = SlackUser.objects.create(
            slack_id="slack_id_3",
            channel_id="channel_id_3",
            has_answered_skill_form=True,
            has_answered_skill_form_v2=False,
            send_no_more_messages=False,
        )
        self.user_4 = SlackUser.objects.create(
            slack_id="slack_id_4",
            channel_id="channel_id_4",
            has_answered_skill_form=True,
            has_answered_skill_form_v2=True,
            send_no_more_messages=False,
        )
        self.user_5 = SlackUser.objects.create(
            slack_id="slack_id_6",
            channel_id="channel_id_6",
            has_answered_skill_form=True,
            has_answered_skill_form_v2=None,
            send_no_more_messages=False,
        )
        self.user_6 = SlackUser.objects.create(
            slack_id="slack_id_5",
            channel_id="channel_id_5",
            has_answered_skill_form=False,
            has_answered_skill_form_v2=False,
            send_no_more_messages=True,
        )

    def test_get_users_to_remind(self):
        """
        Tests that get_users_to_remind gives the correct list of users
        """
        self.assertSequenceEqual(get_users_to_remind(1), [self.user_1, self.user_2])
        self.assertSequenceEqual(
            get_users_to_remind(2), [self.user_1, self.user_3, self.user_5]
        )
