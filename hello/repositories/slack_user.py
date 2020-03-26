"""
Repository methods to access and update slack user models
"""
from hello.models import SlackUser
from hello.api import get_channel_id


def get_all():
    """
    Retrieve the list of all user slack_ids stored in db
    """
    all_user_slack_ids = SlackUser.objects.all()

    return all_user_slack_ids


def save_user_list(all_users_from_slack):
    """
    Add all new users from slack_list to db
    """
    all_user_slack_ids_from_db = [user.slack_id for user in get_all()]

    for user in all_users_from_slack:
        if user["id"] not in all_user_slack_ids_from_db and not user["is_bot"]:
            channel_id = get_channel_id(user["id"])
            if channel_id is not "":
                SlackUser.objects.create(
                    slack_id=user["id"],
                    channel_id=channel_id,
                    has_answered_skill_form=0,
                )
