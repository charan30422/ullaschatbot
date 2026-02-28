"""
WhatsApp Cloud API messaging utility.
Sends text messages via the Meta Graph API.
"""
import logging
import requests
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
    logger.debug("send_message → to=%s body_len=%d", to, len(body))
    logger.debug("send_message → API URL: %s", WHATSAPP_API_URL)
    logger.debug("send_message → Token present: %s", bool(WHATSAPP_TOKEN and WHATSAPP_TOKEN != "YOUR_WHATSAPP_ACCESS_TOKEN"))

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
        logger.info("📤 Sending WhatsApp message to %s ...", to)
        resp = requests.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)

        logger.info("📬 WhatsApp API response: status=%s", resp.status_code)
        logger.debug("📬 WhatsApp API response body: %s", resp.text[:300])

        if resp.status_code == 200:
            logger.info("✅ Message successfully delivered to %s", to)
            return True

        logger.error(
            "❌ WhatsApp API rejected message — status=%s body=%s",
            resp.status_code, resp.text[:300]
        )
        return False

    except requests.exceptions.Timeout:
        logger.error("⏰ Timeout: WhatsApp API did not respond within 10s for recipient %s", to)
        return False

    except requests.exceptions.ConnectionError as exc:
        logger.error("🔌 Connection error sending to %s: %s", to, exc)
        return False

    except requests.exceptions.RequestException as exc:
        logger.error("❌ Request exception sending to %s: %s", to, exc)
        return False
