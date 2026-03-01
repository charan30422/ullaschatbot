"""
Configuration settings for the Ullas WhatsApp Chatbot middleware.
Loads from environment variables / .env file.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# --- Twilio WhatsApp ---
TWILIO_ACCOUNT_SID      = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN       = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER  = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")  # Twilio sandbox default

# --- Webhook verification (keep for Twilio signature validation) ---
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "ullas_verify_token_2026")

# --- Session ---
SESSION_TIMEOUT_SECONDS = int(os.getenv("SESSION_TIMEOUT_SECONDS", "600"))  # 10 minutes

# --- Flask ---
# Render injects PORT automatically; fall back to FLASK_PORT or 10000
FLASK_PORT  = int(os.getenv("PORT", os.getenv("FLASK_PORT", "10000")))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# --- Config Validation Logs (visible at startup in Render) ---
logger.info("📋 Config loaded:")
logger.info("   TWILIO_ACCOUNT_SID     : %s", TWILIO_ACCOUNT_SID[:6] + "***" if TWILIO_ACCOUNT_SID else "❌ NOT SET")
logger.info("   TWILIO_AUTH_TOKEN      : %s", "set" if TWILIO_AUTH_TOKEN else "❌ NOT SET")
logger.info("   TWILIO_WHATSAPP_NUMBER : %s", TWILIO_WHATSAPP_NUMBER)
logger.info("   VERIFY_TOKEN           : %s", VERIFY_TOKEN[:4] + "***" if VERIFY_TOKEN else "❌ NOT SET")
logger.info("   SESSION_TIMEOUT        : %ss", SESSION_TIMEOUT_SECONDS)
logger.info("   FLASK_PORT             : %s", FLASK_PORT)
logger.info("   FLASK_DEBUG            : %s", FLASK_DEBUG)
