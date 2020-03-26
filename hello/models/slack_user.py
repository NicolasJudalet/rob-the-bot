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
    has_answered_skill_form = models.BooleanField()
