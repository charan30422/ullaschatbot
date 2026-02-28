"""
Configuration settings for the Ullas WhatsApp Chatbot middleware.
Loads from environment variables / .env file.
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# --- WhatsApp Business API ---
WHATSAPP_TOKEN   = os.getenv("WHATSAPP_TOKEN", "YOUR_WHATSAPP_ACCESS_TOKEN")
VERIFY_TOKEN     = os.getenv("VERIFY_TOKEN", "ullas_verify_token_2026")
PHONE_NUMBER_ID  = os.getenv("PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"

# --- Session ---
SESSION_TIMEOUT_SECONDS = int(os.getenv("SESSION_TIMEOUT_SECONDS", "600"))  # 10 minutes

# --- Flask ---
# Render injects PORT automatically; fall back to FLASK_PORT or 10000
FLASK_PORT  = int(os.getenv("PORT", os.getenv("FLASK_PORT", "10000")))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# --- Config Validation Logs (visible at startup in Render) ---
logger.info("📋 Config loaded:")
logger.info("   PHONE_NUMBER_ID  : %s", PHONE_NUMBER_ID)
logger.info("   WHATSAPP_API_URL : %s", WHATSAPP_API_URL)
logger.info("   VERIFY_TOKEN     : %s", VERIFY_TOKEN[:4] + "***" if VERIFY_TOKEN else "❌ NOT SET")
logger.info("   WHATSAPP_TOKEN   : %s", ("set (" + str(len(WHATSAPP_TOKEN)) + " chars)") if WHATSAPP_TOKEN and WHATSAPP_TOKEN != "YOUR_WHATSAPP_ACCESS_TOKEN" else "❌ NOT SET / PLACEHOLDER")
logger.info("   SESSION_TIMEOUT  : %ss", SESSION_TIMEOUT_SECONDS)
logger.info("   FLASK_PORT       : %s", FLASK_PORT)
logger.info("   FLASK_DEBUG      : %s", FLASK_DEBUG)
