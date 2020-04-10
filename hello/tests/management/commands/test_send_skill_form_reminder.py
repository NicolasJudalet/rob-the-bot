"""
Test the SendSkillFormReminder command
"""
import datetime

from django.core.management import call_command
from django.test import TestCase
from unittest.mock import call, patch

from hello.models.slack_user import SlackUser


class MockDate(datetime.date):
    @classmethod
    def weekday(cls):
        return 0


class SendSkillFormReminderTest(TestCase):
    def setUp(self):
        self.user_1 = SlackUser.objects.create(
            slack_id="slack_id_1",
            channel_id="channel_id_1",
            has_answered_skill_form=False,
            has_answered_skill_form_v2=False,
            has_answered_skill_form_v2_last_update=None,
            send_no_more_messages=False,
        )
        self.user_2 = SlackUser.objects.create(
            slack_id="slack_id_1",
            channel_id="channel_id_1",
            has_answered_skill_form=False,
            has_answered_skill_form_v2=False,
            has_answered_skill_form_v2_last_update=None,
            send_no_more_messages=False,
        )

    @patch(
        "hello.management.commands.send_skill_form_reminder.create_and_save_from_json_response",
    )
    @patch(
        "hello.management.commands.send_skill_form_reminder.send_message",
        return_value={"json_response"},
    )
    @patch(
        "hello.management.commands.send_skill_form_reminder.get_message_type",
        return_value="message_type",
    )
    @patch(
        "hello.management.commands.send_skill_form_reminder.get_hydrated_message_body",
        return_value="message_body",
    )
    @patch("hello.management.commands.send_skill_form_reminder.get_users_to_remind",)
    def test_handle(
        self,
        get_users_to_remind,
        get_hydrated_message_body,
        get_message_type,
        send_message,
        create_and_save_from_json_response,
    ):
        """
        Tests the command execution
        """
        get_users_to_remind.return_value = [self.user_1, self.user_2]
        call_command("send_skill_form_reminder", 1)

        get_users_to_remind.asset_called_with(1)
        get_hydrated_message_body.assert_called_with(1)
        get_message_type.assert_called_with(1)
        send_message.assert_has_calls(
            [call("message_body", self.user_1), call("message_body", self.user_2)]
        )
        create_and_save_from_json_response.assert_has_calls(
            [
                call({"json_response"}, "message_type", self.user_1),
                call({"json_response"}, "message_type", self.user_2),
            ]
        )

    @patch(
        "hello.management.commands.send_skill_form_reminder.create_and_save_from_json_response",
    )
    @patch(
        "hello.management.commands.send_skill_form_reminder.send_message",
        return_value={"json_response"},
    )
    @patch("hello.management.commands.send_skill_form_reminder.datetime.datetime")
    def test_handle_should_do_nothing_on_dont_send_weekdays(
        self, datetime, send_message, create_and_save_from_json_response,
    ):
        """
        Tests the command only sends messages on the configured weekdays
        """
        with patch(
            "hello.management.commands.send_skill_form_reminder.Command.WEEKDAYS"
        ) as WEEKDAYS_CONSTANT:
            WEEKDAYS_CONSTANT.return_value = ["dont_send_reminder_weekday"]
            datetime.today.return_value = MockDate(2020, 8, 26)
            call_command("send_skill_form_reminder", 2)

            assert not send_message.called, "send_message should not have been called"
            assert (
                not create_and_save_from_json_response.called
            ), "create_and_save_from_json_response should not have been called"
