"""
Implements the authentication system used by slack
https://api.slack.com/docs/verifying-requests-from-slack
"""

import hmac
import os
from hashlib import sha256


def authenticate_call(request):
    """
    Authenticates the response calls from slack
    """
    slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

    basestring = "v0:{}:{}".format(
        request.headers["X-Slack-Request-Timestamp"], request.body.decode("utf-8")
    ).encode("utf-8")

    request_hash = (
        "v0="
        + hmac.new(bytes(slack_signing_secret, "utf-8"), basestring, sha256).hexdigest()
    )

    slack_signature = request.headers["X-Slack-Signature"]

    return hmac.compare_digest(request_hash, slack_signature)
