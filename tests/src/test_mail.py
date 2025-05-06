from src.mail import send_email, _set_mailjet_api_auth, _create_email_payload
from unittest.mock import MagicMock, patch
import pytest


def test_send_email() -> None:
    """
    Test the send_email function.
    """

    to_email = "sample@mail.com"
    body = "This is a test email from Python."
    subject = "Test Email from Python"

    with (
        patch("src.mail.os") as mock_os,
        patch("src.mail.requests.Session") as mock_session,
    ):
        mock_os.environ.get.return_value = {
            "MAILJET_API_KEY": "test_key",
            "MAILJET_API": "test_secret",
            "FROM_EMAIL": "from@mail.com",
        }
        mock_session.return_value.__enter__.return_value = mock_session
        mock_session.return_value.post.return_value = MagicMock(
            status_code=200, text="Email sent successfully"
        )

        send_email(
            to_email=to_email,
            body=body,
            subject=subject,
        )


def test_send_email_no_env_vars_set() -> None:
    """
    Test the send_email function.
    """
    with (
        patch("src.mail.os") as mock_os,
        patch("src.mail.requests.Session"),
        pytest.raises(
            ValueError,
            match="MAILJET_API_KEY or MAILJET_API_SECRET environment variables not set.",
        ),
    ):
        mock_os.environ = {}
        send_email(
            to_email="to_email",
            body="body",
            subject="subject",
        )


def test_send_email_no_from_set() -> None:
    """
    Test the send_email function.
    """
    with (
        patch("src.mail.os") as mock_os,
        patch("src.mail.requests.Session"),
        pytest.raises(
            ValueError,
            match="FROM_EMAIL environment variable not set.",
        ),
    ):
        mock_os.environ = {
            "MAILJET_API_KEY": "test_key",
            "MAILJET_API_SECRET": "test_secret",
            "FROM_EMAIL": None,
        }
        send_email(
            to_email="to_email",
            body="body",
            subject="subject",
        )


def test_set_mailjet_api_auth() -> None:
    """
    Test the _set_mailjet_api_auth function.
    """
    api_key = "test_key"
    api_secret = "test_secret"
    with patch("src.mail.os") as mock_os:
        mock_os.environ = {
            "MAILJET_API_KEY": api_key,
            "MAILJET_API_SECRET": api_secret,
        }
        received_api_key, received_api_secret = _set_mailjet_api_auth()
        assert received_api_key == api_key
        assert received_api_secret == api_secret

def test_set_mailjet_api_auth_missing_key() -> None:
    """
    Test the _set_mailjet_api_auth function.
    """
    with (patch("src.mail.os") as mock_os, 
          pytest.raises(
              ValueError,
              match="MAILJET_API_KEY or MAILJET_API_SECRET environment variables not set.",
          )):
        mock_os.environ = {}
        _set_mailjet_api_auth()


def test_create_email_payload() -> None:
    """
    Test the _create_email_payload function.
    """
    from_email = "sample@mail.com"
    to_email = "sample_to@mail.com"
    body = "This is a test email from Python."
    subject = "Test Email from Python"
    
    expected_payload = {
        "Messages": [
            {
                "From": {"Email": from_email},
                "To": [{"Email": to_email}],
                "Subject": subject,
                "TextPart": body,
            }
        ]
    }
    payload = _create_email_payload(from_email, to_email, body, subject)
    assert payload == expected_payload
