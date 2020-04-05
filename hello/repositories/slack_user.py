"""
Repository methods to access and update slack user models
"""
from django.db.models import Q
from hello.models.slack_user import SlackUser
from hello.api.slack import get_channel_id


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
            if channel_id != "":
                SlackUser.objects.create(
                    slack_id=user["id"], channel_id=channel_id,
                )


def update_status(slack_id, message_type_id, has_answered_form, send_no_more_messages):
    """
    Update the user status with received answer
    """
    MAPPING = {"1": "has_answered_skill_form", "2": "has_answered_skill_form_v2"}
    if send_no_more_messages:
        SlackUser.objects.filter(slack_id=slack_id).update(
            send_no_more_messages=send_no_more_messages
        )
    else:
        SlackUser.objects.filter(slack_id=slack_id).update(
            **{MAPPING[str(message_type_id)]: has_answered_form}
        )


def get_users_to_remind(message_type_id):
    """
    Returns the list of users who have not filled the form yet (in the version
    corresponding to message_type_id) and have not asked to receive no more messages
    """
    MAPPING = {"1": "has_answered_skill_form", "2": "has_answered_skill_form_v2"}
    return SlackUser.objects.filter(
        ~Q(**{MAPPING[str(message_type_id)]: True}), Q(send_no_more_messages=False),
    )
