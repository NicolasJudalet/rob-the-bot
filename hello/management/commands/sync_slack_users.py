"""
The Sync Slack Users List Command
"""

from django.core.management.base import BaseCommand

from hello.api.slack import get_all_users
from hello.repositories.slack_user import save_user_list


class Command(BaseCommand):
    """
    This command is triggered each day, before sending the Skill Form Reminder command.
    Its goal is to update the list of slack users in db
    to synchronize it with the latest data from slack
    """

    help = (
        "Gets the list of all slack workspace users "
        "and synchronize the app db by creating and saving "
        "all SlackUser entities if they do not exist yet"
    )

    def handle(self, *args, **kwargs):
        all_users_from_slack = get_all_users()
        save_user_list(all_users_from_slack)
