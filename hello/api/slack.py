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
    I_LEAVE_YOU_IN_PEACE_MESSAGE,
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


def send_message(message_body, user):
    """
    Sends a message to the user
    """
    message_with_channel_id = message_body.replace("___channel_id___", user.channel_id)
    try:
        response = requests.post(
            "{}/chat.postMessage".format(os.environ.get("SLACK_BASE_URL")),
            headers={
                "Authorization": "Bearer {}".format(os.environ.get("SLACK_TOKEN")),
                "Content-type": "application/json",
            },
            data=message_with_channel_id,
        )

        return json.loads(response.content)

    except Exception:
        logger = logging.getLogger()
        logger.error(
            "Could not send reminder message to user with slack_id %s", user.slack_id,
        )


def send_acknowledged_message(
    message_id, response_url, message_body, has_answered_form, send_no_more_messages,
):
    """
    Sends a message acknowledgement to the user
    """
    if send_no_more_messages:
        acknowledgement_reponse = I_LEAVE_YOU_IN_PEACE_MESSAGE
    elif has_answered_form:
        acknowledgement_reponse = THANK_YOU_MESSAGE
    else:
        acknowledgement_reponse = I_WILL_BE_BACK_MESSAGE

    acknowledged_message_body = message_body.replace(
        "___acknowledgement_response___", acknowledgement_reponse
    )
    try:
        requests.post(
            response_url,
            headers={
                "Authorization": "Bearer {}".format(os.environ.get("SLACK_TOKEN")),
                "Content-type": "application/json",
            },
            data=acknowledged_message_body,
        )

    except Exception:
        logger = logging.getLogger()
        logger.error(
            "Could not send message acknowledgement for message with id %s", message_id,
        )
