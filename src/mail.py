import logging
import os

import requests

logging.basicConfig(level=logging.INFO)


def send_email(to_email: str, body: str, subject:str) -> None:
    """
    Send an email using Mailjet via HTTP API and requests.

    Args:
        to_email (str): Recipient's email.
        body (str): The plain text body of the email.
    """
    api_key, api_secret = _set_mailjet_api_auth()

    from_email = os.environ.get("FROM_EMAIL")
    
    if not from_email:
        raise ValueError("FROM_EMAIL environment variable not set.")
    
    with requests.Session() as session:
        session.auth = (api_key, api_secret)
        session.headers.update({"Content-Type": "application/json"})
        response = session.post(
            "https://api.mailjet.com/v3.1/send",
            json=_create_email_payload(from_email, to_email, body, subject),
        )
    
    response.raise_for_status() 
    logging.info(f"Response: {response.status_code} - {response.text}")

def _set_mailjet_api_auth() -> tuple[str, str]:
    """
    Set the Mailjet API authentication.

    Returns:
        tuple: A tuple containing the API key and secret.
    """
    api_key = os.environ.get("MAILJET_API_KEY")
    api_secret = os.environ.get("MAILJET_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "MAILJET_API_KEY or MAILJET_API_SECRET environment variables not set."
        )

    return api_key, api_secret

def _create_email_payload(from_email: str, to_email: str, body: str, subject: str) -> dict:
    """
    Create the payload for the email.

    Args:
        from_email (str): Sender's email.
        to_email (str): Recipient's email.
        body (str): The plain text body of the email.
        subject (str): The subject of the email.

    Returns:
        dict: The payload for the email.
    """
    return {
        "Messages": [
            {
                "From": {"Email": from_email},
                "To": [{"Email": to_email}],
                "Subject": subject,
                "TextPart": body,
            }
        ]
    }


if __name__ == "__main__":
    send_email(
        to_email="ivo.lindsen@gmail.com",
        body="This is a test email from Python App2.",
        subject="Test Email from Python App2",
    )
