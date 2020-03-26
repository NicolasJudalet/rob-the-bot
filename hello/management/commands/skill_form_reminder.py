"""
The Skill Form Reminder Command
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from hello.api import get_all_users


class Command(BaseCommand):
    """
    This command is triggered each day.
    Its goal is to remind volunteers who have not filled the skill form yet to do so.
    """

    help = (
        "Gets the list of all workspace users, "
        "checks which ones have not filled the skill form yet "
        "and sends them a reminder"
    )

    def handle(self, *args, **kwargs):
        # time = timezone.now().strftime("%X")
        # self.stdout.write("It's now %s" % time)
        all_users = get_all_users()
        print(all_users)
