"""
Repository methods to access and update MessageType objects
"""
import json
import os
from gettingstarted.settings import BASE_DIR
from hello.models.message_type import MessageType


def get_hydrated_message_body(message_type_id):
    MESSAGE_TEMPLATES_DIR = "{}/hello/api/payload_templates".format(BASE_DIR)

    message_type = get(message_type_id)
    message_template_file = os.path.join(
        MESSAGE_TEMPLATES_DIR, message_type.template_file
    )

    with open(message_template_file) as f:
        message_body = (
            json.dumps(json.load(f))
            .replace("___skill_form_url___", os.environ.get("SKILL_FORM_URL"))
            .replace("___form_icon_url___", os.environ.get("FORM_ICON_URL"))
        )

    return message_body


def get(message_type_id):
    return MessageType.objects.get(pk=message_type_id)
