"""
Serializers to format payloads from and to slacks
"""
import json


def deserialize_reminder_payload(request):
    """
    Deserializes the payload sent in slack POST request when users answer the reminder
    """
    return json.loads(dict(request.POST)["payload"][0])
