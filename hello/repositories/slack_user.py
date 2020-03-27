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


def update_status(slack_id, has_answered_skill_form):
    """
    Update the user status with received answer
    """
    SlackUser.objects.filter(slack_id=slack_id).update(
        has_answered_skill_form=has_answered_skill_form
    )


def get_users_to_remind():
    """
    Returns the list of users who have not filled the form yet
    """
    return SlackUser.objects.filter(has_answered_skill_form=False)
