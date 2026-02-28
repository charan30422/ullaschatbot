"""
WhatsApp Cloud API messaging utility.
Sends text messages via the Meta Graph API.
"""
import logging
import requests
import requests.exceptions
from config import WHATSAPP_API_URL, WHATSAPP_TOKEN

logger = logging.getLogger(__name__)


def send_message(to: str, body: str) -> bool:
    """
    Send a text message to a WhatsApp number via the Cloud API.

    Args:
        to:   recipient phone number in international format (e.g. "919876543210")
        body: message text (supports WhatsApp markdown: *bold*, _italic_)

    Returns:
        True if the API accepted the message, False otherwise.
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body},
    }

    try:
        resp = requests.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)

        # Meta returns 200 on success
        if resp.status_code == 200:
            logger.info("✅ Message sent to %s", to)
            return True

        logger.error("❌ WhatsApp API error %s: %s", resp.status_code, resp.text)
        return False

    except requests.exceptions.Timeout:
        logger.error("❌ Timeout sending message to %s (10s limit exceeded)", to)
        return False

    except requests.exceptions.RequestException as exc:
        logger.error("❌ Failed to send message to %s: %s", to, exc)
        return False
