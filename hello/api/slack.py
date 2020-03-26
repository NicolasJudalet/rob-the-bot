"""
All api calls to Slack
"""

import json
import os
import requests


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
