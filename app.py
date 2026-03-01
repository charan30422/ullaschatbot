"""
Ullas Student WhatsApp Chatbot — Flask Middleware
=================================================
Simplified flow: Hi → Menu → Answer (no Ullas ID required)
"""
import logging
import sys
from flask import Flask, request, jsonify

from config import FLASK_PORT, FLASK_DEBUG
from handlers import MAIN_MENU, MENU_HANDLERS, talk_to_support
from whatsapp import send_message

# ---- Logging ----
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("🚀  Ullas WhatsApp Chatbot — starting up (Twilio)")
logger.info("    FLASK_PORT  : %s", FLASK_PORT)
logger.info("    FLASK_DEBUG : %s", FLASK_DEBUG)
logger.info("=" * 60)

app = Flask(__name__)


# ===================================================================
#  ROUTES
# ===================================================================

@app.route("/health", methods=["GET"])
def health():
    logger.info("🏥 /health — ok")
    return jsonify({"status": "ok", "service": "ullas-whatsapp-chatbot"})


@app.route("/webhook", methods=["POST"])
def handle_message():
    """Receive incoming WhatsApp messages from Twilio (form-encoded POST)."""
    body   = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")
    logger.info("📥 From=%s Body=[%s]", sender, body)

    if not sender or not body:
        logger.warning("⚠️ Missing From or Body — ignoring")
        return "", 200

    # Normalise phone number (strip whatsapp:+ prefix)
    phone = sender.replace("whatsapp:+", "").replace("whatsapp:", "").lstrip("+")

    try:
        _process_message(phone, body)
    except Exception:
        logger.exception("💥 Unhandled exception")

    return "", 200


# ===================================================================
#  MESSAGE PROCESSING
# ===================================================================

def _process_message(phone: str, text: str) -> None:
    """
    Simple flow — no Ullas ID required:
      Hi / Hello / start / menu  →  show main menu
      1–6                        →  show answer for that option
      7                          →  talk to support
      anything else              →  show main menu
    """
    text_lower = text.lower().strip()
    logger.info("🔄 Processing — phone=%s text=[%s]", phone, text)

    # ---- Greetings / Menu keywords → show menu ----
    if text_lower in ("hi", "hello", "hey", "start", "menu", "back", "main menu", "0"):
        logger.info("🏠 Showing main menu to %s", phone)
        send_message(phone, MAIN_MENU)
        return

    # ---- Menu options 1–6 ----
    if text in MENU_HANDLERS:
        label, handler = MENU_HANDLERS[text]
        logger.info("📋 Option %s (%s) selected by %s", text, label, phone)
        try:
            response = handler()
            logger.debug("📋 Response preview: %s", response[:80])
        except Exception:
            logger.exception("💥 Handler for option %s failed", text)
            response = "⚠️ Something went wrong. Please try again.\n\n_Reply *menu* to go back._"
        send_message(phone, response)
        return

    # ---- Option 7 — Support ----
    if text == "7":
        logger.info("📞 Support selected by %s", phone)
        send_message(phone, talk_to_support())
        return

    # ---- Anything else → show menu ----
    logger.info("🤔 Unrecognised input [%s] from %s — showing menu", text, phone)
    send_message(
        phone,
        "🤔 I didn't understand that.\n\n"
        "Please reply with a number *1–7* to choose an option:\n\n"
        + MAIN_MENU
    )


# ===================================================================
#  ENTRY POINT
# ===================================================================

if __name__ == "__main__":
    logger.info("🚀 Starting Flask dev server on port %s", FLASK_PORT)
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
