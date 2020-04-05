"""
All the app views
"""
import logging
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from hello.api.slack import send_reminder_acknowledgement
from hello.authentication.slack import authenticate_call
from hello.DTO.slack_event_payload import SlackEventPayload
from hello.models.greeting import Greeting
from hello.repositories.slack_user import update_status
from hello.repositories.message import get_message_type_id_from_actions_block
from hello.serializers import deserialize_reminder_user_response_payload


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
    if not authenticate_call(request):
        return HttpResponse("Failed authentication", status=403)

    try:
        payload = deserialize_reminder_user_response_payload(request)
        slack_event_payload = SlackEventPayload(payload)
        message_type_id = get_message_type_id_from_actions_block(
            slack_event_payload.actions_block_id
        )

        update_status(
            slack_event_payload.user_slack_id,
            message_type_id,
            slack_event_payload.has_answered_form,
            slack_event_payload.send_no_more_messages,
        )

        send_reminder_acknowledgement(
            slack_event_payload.response_url, slack_event_payload.has_answered_form
        )

        return HttpResponse("Response successfully stored!")

    except KeyError:
        logger = logging.getLogger()
        error_message = "Could not deserialize response from slack:\n{}".format(
            request.POST
        )
        logger.error(error_message)

        return HttpResponse(error_message, status=500)
