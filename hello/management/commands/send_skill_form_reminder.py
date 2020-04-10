"""
Command used to send the Skill Form Reminder message
to all the volunteers who have not answered it yet
"""
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from hello.api.slack import send_message
from hello.repositories.slack_user import get_users_to_remind
from hello.repositories.message import create_and_save_from_json_response
from hello.repositories.message_type import (
    get as get_message_type,
    get_hydrated_message_body,
)


class Command(BaseCommand):
    """
    This command is triggered each day, after the Sync Slack Users command.
    Its triggers a reminder message for all users who have not answered the
    skills form yet
    """

    help = (
        "Gets the list of all slack workspace users "
        "who have not answered the form (stored in DB) "
        "and send them a private message reminder on Slack"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "message-type-id", type=int, help="The id of the type of message to send"
        )

    WEEKDAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def handle(self, *args, **kwargs):
        current_day_of_week = self.WEEKDAYS[datetime.datetime.today().weekday()]
        if current_day_of_week in settings.SEND_REMINDER_WEEKDAYS:
            message_type_id = kwargs["message-type-id"]

            all_users_to_remind = get_users_to_remind(message_type_id)
            message_body = get_hydrated_message_body(message_type_id)
            message_type = get_message_type(message_type_id)

            for user in all_users_to_remind:
                try:
                    json_response = send_message(message_body, user)
                    create_and_save_from_json_response(
                        json_response, message_type, user
                    )
                except KeyError:
                    logger = logging.getLogger()
                    error_message = "Could not deserialize response from slack for user {}:\n{}".format(
                        user.slack_id, json_response
                    )
                    logger.error(error_message)
