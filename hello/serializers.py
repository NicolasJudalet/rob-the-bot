"""
Serializers to format payloads from and to slacks
"""
import json


def deserialize_reminder_user_response_payload(request):
    """
    Deserializes the payload sent in slack POST request when users answer the reminder
    """
    return json.loads(dict(request.POST)["payload"][0])


def get_actions_block_id_from_reminder_response_payload(json_response):
    """
    Gets the actions_block_id from the payload sent by slack in response to reminder message v1
    """
    return json_response["message"]["blocks"][4]["block_id"]
