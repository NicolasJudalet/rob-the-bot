"""
Command used to send the Skill Form Reminder message
to all the volunteers who have not answered it yet
"""

from django.core.management.base import BaseCommand

from hello.api import send_reminder
from hello.repositories.slack_user import get_users_to_remind


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

    def handle(self, *args, **kwargs):
        all_users_to_remind = get_users_to_remind()
        send_reminder(all_users_to_remind)
