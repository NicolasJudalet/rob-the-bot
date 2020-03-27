"""
All the app views
"""
import logging
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .api.constants import FORM_FILLED
from .models import Greeting
from .repositories.slack_user import update_status
from .serializers import deserialize_reminder_payload


def index(request):
    """
    The index view (not used, from boilerplate)
    """
    times = int(os.environ.get("TIMES", 3))
    return HttpResponse("Hello! " * times)


def db(request):
    """
    The db view (not used, from boilerplate)
    """
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


@csrf_exempt
def slack(request):
    """
    Handles the reminder reponse call from Slack
    """
    try:
        payload = deserialize_reminder_payload(request)

        user_slack_id = payload["user"]["id"]
        has_answered_skill_form = payload["actions"][0]["value"] == FORM_FILLED
        update_status(user_slack_id, has_answered_skill_form)

        return HttpResponse("Response successfully stored !")

    except KeyError:
        logger = logging.getLogger()
        error_message = "Could not deserialize response from slack for user {}".format(
            user_slack_id
        )
        logger.error()

        return HttpResponse(error_message, status=500)
