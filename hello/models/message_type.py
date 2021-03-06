"""
The Message Type model
"""
from django.db import models


class MessageType(models.Model):
    """
    DB entities corresponding to message types
    """

    name = models.CharField(max_length=64)
    template_file = models.CharField(max_length=128)
