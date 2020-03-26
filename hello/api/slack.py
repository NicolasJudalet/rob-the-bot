"""
All api calls to Slack
"""

import json
import logging
import os
import requests

from .constants import HTTP_STATUS_TOO_MANY_REQUESTS


def get_all_users():
    """
    Get a list of all slack users
    """
    url = "{}/users.list".format(os.environ.get("SLACK_BASE_URL"))
    response = requests.get(
        url,
        headers={"Authorization": "Bearer {}".format(os.environ.get("SLACK_TOKEN"))},
    )

    return json.loads(response.content)["members"]


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
