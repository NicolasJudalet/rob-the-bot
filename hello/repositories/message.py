"""
Repository methods to access, create and update Message objects
"""
from time import timezone

from hello.models.slack_message import SlackMessage
from hello.serializers import get_actions_block_id_from_reminder_response_payload


def create_and_save_from_json_response(json_response, message_type, user):
    SlackMessage.objects.create(
        user=user,
        message_type=message_type,
        actions_block_id=get_actions_block_id_from_reminder_response_payload(
            json_response
        ),
    )


def get_message_type_id_from_actions_block(actions_block_id):
    message = next(
        iter(SlackMessage.objects.all().filter(actions_block_id=actions_block_id)), None
    )  # gets the first element of the queryset or None if the list is empty
    return message.message_type.id if message else 1


def update_status(actions_block_id, response_url):
    message = next(
        iter(SlackMessage.objects.all().filter(actions_block_id=actions_block_id)), None
    )

    if message:
        message.update(
            answered_at=timezone.now, response_url=response_url,
        )
        return message.id
    else:
        return None
