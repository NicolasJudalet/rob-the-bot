"""
All api calls to Slack
"""

import json
import logging
import os
import requests

from gettingstarted.settings import BASE_DIR
from .constants import (
    HTTP_STATUS_TOO_MANY_REQUESTS,
    THANK_YOU_MESSAGE,
    I_WILL_BE_BACK_MESSAGE,
)


def get_all_users():
    """
    Get a list of all slack users
    """
    try:
        url = "{}/users.list".format(os.environ.get("SLACK_BASE_URL"))
        response = requests.get(
            url,
            headers={
                "Authorization": "Bearer {}".format(os.environ.get("SLACK_TOKEN"))
            },
        )

        return json.loads(response.content)["members"]
    except KeyError:
        logger = logging.getLogger()
        logger.error(
            'Received response does not contain "members" key : \n%s', response.content
        )


def get_channel_id(user_slack_id):
    url = "{}/conversations.open".format(os.environ.get("SLACK_BASE_URL"))
    response = requests.post(
        url,
        headers={"Authorization": "Bearer {}".format(os.environ.get("SLACK_TOKEN"))},
        data={"users": user_slack_id},
    )

    if response.status_code == HTTP_STATUS_TOO_MANY_REQUESTS:
        logger = logging.getLogger()
        logger.error(
            (
                "Number of requests exceeding rate limit of Slack API: ",
                "try triggering the command again in 30s",
            )
        )
        return ""

    try:
        return json.loads(response.content)["channel"]["id"]
    except KeyError:
        logger = logging.getLogger()
        logger.error(
            "Could not get channel id for user with following slack id : %s",
            user_slack_id,
        )
        return ""


def send_reminder_acknowledgement(response_url, has_answered_skill_form):
    """
    Sends an acknowledgement to Slack after receiving user response to reminder
    """
    message_template_file = "{}/hello/api/payload_templates/acknowledged_reminder_message_payload.json".format(
        BASE_DIR
    )
    with open(message_template_file) as f:
        response_body = json.dumps(json.load(f)).replace(
            "___acknowledgement_response___",
            THANK_YOU_MESSAGE if has_answered_skill_form else I_WILL_BE_BACK_MESSAGE,
        )

    requests.post(
        response_url,
        headers={
            "Authorization": "Bearer {}".format(os.environ.get("SLACK_TOKEN")),
            "Content-type": "application/json",
        },
        data=response_body,
    )
