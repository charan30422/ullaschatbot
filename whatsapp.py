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

# --- Module-level Twilio client (created once at startup, not per request) ---
_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Pre-compute the From number at startup
_raw = TWILIO_WHATSAPP_NUMBER.strip()
if _raw.startswith("whatsapp:"):
    _FROM = _raw
elif _raw.startswith("+"):
    _FROM = f"whatsapp:{_raw}"
else:
    _FROM = f"whatsapp:+{_raw}"

logger.info("📱 Twilio client ready — from=%s", _FROM)


def send_message(to: str, body: str) -> bool:
    """
    Send a WhatsApp message via Twilio.
    Uses the module-level client singleton for speed.
    """
    to_formatted = f"whatsapp:+{to.lstrip('+')}" 
    logger.info("📤 Sending to %s", to_formatted)

    try:
        message = _client.messages.create(
            body=body,
            from_=_FROM,
            to=to_formatted,
        )
        logger.info("✅ Sent! SID=%s", message.sid)
        return True

    except Exception as exc:
        logger.error("❌ Twilio send failed to %s: %s", to, exc)
        return False
