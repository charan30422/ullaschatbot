"""
Configuration settings for the Ullas WhatsApp Chatbot middleware.
Loads from environment variables / .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- WhatsApp Business API ---
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "YOUR_WHATSAPP_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "ullas_verify_token_2026")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"

# --- Session ---
SESSION_TIMEOUT_SECONDS = int(os.getenv("SESSION_TIMEOUT_SECONDS", "600"))  # 10 minutes

# --- Flask ---
# Render injects PORT automatically; fall back to FLASK_PORT or 10000
FLASK_PORT = int(os.getenv("PORT", os.getenv("FLASK_PORT", "10000")))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
