"""
The Slack message model
"""
from django.db import models
from django.utils import timezone
from hello.models.slack_user import SlackUser
from hello.models.message_type import MessageType


class SlackMessage(models.Model):
    """
    DB entities corresponding to messages sent to the Slack workspace
    """

    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
    message_type = models.ForeignKey(MessageType, on_delete=models.DO_NOTHING)
    actions_block_id = models.CharField(max_length=128, null=True, blank=True)
    sent_at = models.DateTimeField(default=timezone.now)
    answered_at = models.DateTimeField(null=True, blank=True)
    response_url = models.CharField(max_length=256, null=True, blank=True)
