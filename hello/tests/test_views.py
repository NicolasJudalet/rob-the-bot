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

    @patch("hello.views.send_acknowledged_message")
    @patch(
        "hello.views.get_hydrated_message_body", return_value="hydrated_message_body"
    )
    @patch("hello.views.update_message_status", return_value=1)
    @patch("hello.views.update_user_status")
    @patch("hello.views.get_message_type_id_from_actions_block", return_value=2)
    @patch(
        "hello.views.deserialize_reminder_user_response_payload",
        return_value={
            "user": {"id": "SLACK_ID"},
            "response_url": "https://slack.com/response_url",
            "actions": [{"block_id": "BLOCK_ID", "value": "form_not_filled",}],
        },
    )
    @patch("hello.views.authenticate_call", return_value=True)
    def test_slack(
        self,
        authenticate_call,
        deserialize_reminder_user_response_payload,
        get_message_type_id_from_actions_block,
        update_user_status,
        update_message_status,
        get_hydrated_message_body,
        send_acknowledged_message,
    ):
        """
        Tests the slack endpoint
        NB:This also tests the logic inside the SlackEventPayload DTO constructor
        """
        request = self.factory.post(
            "/api/slack", data=self.request_payload, content_type="application/json"
        )

        response = slack(request)

        authenticate_call.assert_called_with(request)
        deserialize_reminder_user_response_payload.assert_called_with(request)
        get_message_type_id_from_actions_block.assert_called_with("BLOCK_ID")
        update_user_status.assert_called_with("SLACK_ID", 2, False, False)
        update_message_status.assert_called_with(
            "BLOCK_ID", "https://slack.com/response_url"
        )
        get_hydrated_message_body.assert_called_with(2, acknowledgement=True)
        send_acknowledged_message.assert_called_with(
            1, "https://slack.com/response_url", "hydrated_message_body", False, False
        )
        self.assertEqual(response.status_code, 200)

    @patch("hello.views.send_acknowledged_message")
    @patch("hello.views.update_user_status")
    @patch("hello.views.deserialize_reminder_user_response_payload",)
    @patch("hello.views.authenticate_call", return_value=False)
    def test_unauthenticated_call(
        self,
        authenticate_call,
        deserialize_reminder_user_response_payload,
        update_user_status,
        send_acknowledged_message,
    ):
        """Tests unauthenticated calls get answered 403 and are not processed"""
        request = self.factory.post(
            "/api/slack", data=self.request_payload, content_type="application/json"
        )

        response = slack(request)

        authenticate_call.assert_called_with(request)
        assert (
            not deserialize_reminder_user_response_payload.called
        ), "deserialize_reminder_user_response_payload should not have been called"
        assert (
            not update_user_status.called
        ), "update_user_status should not have been called"
        assert (
            not send_acknowledged_message.called
        ), "send_acknowledged_message should not have been called"
        self.assertEqual(response.status_code, 403)
