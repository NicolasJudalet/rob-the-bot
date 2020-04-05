"""
Data Transfer Object containing the useful information sent in slack events
(like user responding to a reminder message)
"""
from hello.api.constants import FORM_FILLED, SEND_NO_MORE_MESSAGES


class SlackEventPayload:
    def __init__(self, payload):
        self.user_slack_id = payload["user"]["id"]
        self.actions_block_id = payload["actions"][0]["block_id"]
        self.has_answered_form = payload["actions"][0]["value"] == FORM_FILLED
        self.send_no_more_messages = (
            payload["actions"][0]["value"] == SEND_NO_MORE_MESSAGES
        )
        self.response_url = payload["response_url"]
