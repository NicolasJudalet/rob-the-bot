"""
Repository methods to access and update MessageType objects
"""
import json
import os
from django.conf import settings
from hello.models.message_type import MessageType


def get_hydrated_message_body(message_type_id, acknowledgement=False):
    MESSAGE_TEMPLATES_DIR = "{}/hello/api/payload_templates".format(settings.BASE_DIR)
    SKILL_FORM_URL_MAPPING = {
        1: "SKILL_FORM_URL",
        2: "SKILL_FORM_V2_URL",
    }

    message_type = get(message_type_id)
    message_template_file = os.path.join(
        MESSAGE_TEMPLATES_DIR,
        message_type.template_file
        if not acknowledgement
        else "acknowledged_" + message_type.template_file,
    )

    with open(message_template_file) as f:
        message_body = (
            json.dumps(json.load(f))
            .replace(
                "___skill_form_url___",
                os.environ.get(SKILL_FORM_URL_MAPPING.get(message_type_id)),
            )
            .replace("___form_icon_url___", os.environ.get("FORM_ICON_URL"))
        )

    return message_body


def get(message_type_id):
    return MessageType.objects.get(pk=message_type_id)
