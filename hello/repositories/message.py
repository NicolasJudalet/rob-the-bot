"""
Repository methods to access, create and update Message objects
"""

from hello.models import SlackMessage
from hello.serializers import get_actions_block_id_from_reminder_response_payload

def create_and_save_from_json_response(json_response, message_type, user):
    SlackMessage.objects.create(
        user = user,
        message_type = message_type,
        actions_block_id = get_actions_block_id_from_reminder_response_payload(json_response),
    )