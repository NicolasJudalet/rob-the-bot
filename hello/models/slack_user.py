"""
The Slack user model
"""
from django.db import models

# Create your models here.
class SlackUser(models.Model):
    """
    DB entities corresponding to users in the Slack workspace
    """

    slack_id = models.CharField(max_length=128)
    channel_id = models.CharField(max_length=128)
    has_answered_skill_form = models.BooleanField(default=False)
    has_answered_skill_form_v2 = models.BooleanField(blank=True, null=True)
    has_answered_skill_form_v2_last_update = models.DateTimeField(blank=True, null=True)
    send_no_more_messages = models.BooleanField(default=False)