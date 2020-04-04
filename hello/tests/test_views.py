"""
Tests for the app views
"""
from unittest.mock import patch

from django.test import TestCase, RequestFactory

from hello.views import slack


class TestSlack(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.request_payload = {
            "payload": [
                {
                    "user": {"id": "SLACK_ID"},
                    "response_url": "https://slack.com/response_url",
                    "actions": [{"value": "form_not_filled",}],
                }
            ]
        }

    @patch("hello.views.send_reminder_acknowledgement")
    @patch("hello.views.update_status")
    @patch(
        "hello.views.deserialize_reminder_payload",
        return_value={
            "user": {"id": "SLACK_ID"},
            "response_url": "https://slack.com/response_url",
            "actions": [{"value": "form_not_filled",}],
        },
    )
    @patch("hello.views.authenticate_call", return_value=True)
    def test_slack(
        self,
        authenticate_call,
        deserialize_reminder_payload,
        update_status,
        send_reminder_acknowledgement,
    ):
        """Tests the slack endpoint"""
        request = self.factory.post(
            "/api/slack", data=self.request_payload, content_type="application/json"
        )

        response = slack(request)

        authenticate_call.assert_called_with(request)
        deserialize_reminder_payload.assert_called_with(request)
        update_status.assert_called_with("SLACK_ID", False)
        send_reminder_acknowledgement.assert_called_with(
            "https://slack.com/response_url", False
        )
        self.assertEqual(response.status_code, 200)

    @patch("hello.views.send_reminder_acknowledgement")
    @patch("hello.views.update_status")
    @patch(
        "hello.views.deserialize_reminder_payload",
        return_value={
            "user": {"id": "SLACK_ID"},
            "response_url": "https://slack.com/response_url",
            "actions": [{"value": "form_not_filled",}],
        },
    )
    @patch("hello.views.authenticate_call", return_value=False)
    def test_unauthenticated_call(
        self,
        authenticate_call,
        deserialize_reminder_payload,
        update_status,
        send_reminder_acknowledgement,
    ):
        """Tests unauthenticated calls get answered 403 and are not processed"""
        request = self.factory.post(
            "/api/slack", data=self.request_payload, content_type="application/json"
        )

        response = slack(request)

        authenticate_call.assert_called_with(request)
        assert (
            not deserialize_reminder_payload.called
        ), "deserialize_reminder_payload should not have been called"
        assert not update_status.called, "update_status should not have been called"
        assert (
            not send_reminder_acknowledgement.called
        ), "send_reminder_acknowledgement should not have been called"
        self.assertEqual(response.status_code, 403)
