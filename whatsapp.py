"""
WhatsApp messaging utility — powered by Twilio.
Sends text messages via the Twilio WhatsApp Sandbox API.
"""
import logging
from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_NUMBER,
)

logger = logging.getLogger(__name__)


def send_message(to: str, body: str) -> bool:
    """
    Send a WhatsApp message via Twilio.

    Args:
        to:   recipient phone number in international format (e.g. "919876543210")
        body: message text

    Returns:
        True if message was accepted by Twilio, False otherwise.
    """
    logger.debug("send_message → to=%s body_len=%d", to, len(body))
    logger.debug("send_message → from=%s", TWILIO_WHATSAPP_NUMBER)
    logger.debug("send_message → Account SID present: %s", bool(TWILIO_ACCOUNT_SID))

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Twilio requires "whatsapp:+<number>" format
        to_formatted   = f"whatsapp:+{to.lstrip('+')}"
        from_formatted = TWILIO_WHATSAPP_NUMBER  # already in whatsapp:+1415... format

        logger.info("📤 Sending WhatsApp message to %s via Twilio ...", to_formatted)

        message = client.messages.create(
            body=body,
            from_=from_formatted,
            to=to_formatted,
        )

        logger.info("✅ Message sent! SID=%s status=%s", message.sid, message.status)
        return True

    except Exception as exc:
        logger.error("❌ Twilio send failed to %s: %s", to, exc)
        return False
