"""
Ullas Student WhatsApp Chatbot — Flask Middleware
=================================================
Entry point. Handles Twilio WhatsApp webhook & incoming messages.
Routes messages through authentication → menu → query handlers.
"""
import logging
import sys
from flask import Flask, request, jsonify

from config import FLASK_PORT, FLASK_DEBUG
from auth import (
    get_session,
    start_session,
    lookup_student,
    touch_session,
    clear_session,
)
from handlers import MAIN_MENU, MENU_HANDLERS, talk_to_support
from whatsapp import send_message

# ---- Logging — stream to stdout so Render captures it ----
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

# Greeting message shown to new / returning users
_WELCOME_MSG = (
    "Welcome to Ullas Support! 👋\n\n"
    "To get started, please enter your:\n"
    "🆔 *Ullas ID* (e.g. UL-09-2026-00456)\n\n"
    "or\n\n"
    "📱 *Registered Mobile Number* (e.g. 919876543210)"
)


# ===================================================================
#  ROUTES
# ===================================================================

@app.route("/health", methods=["GET"])
def health():
    """Simple health check — used by Render and uptime monitors."""
    logger.info("🏥 /health called — responding ok")
    return jsonify({"status": "ok", "service": "ullas-whatsapp-chatbot"})


@app.route("/webhook", methods=["POST"])
def handle_message():
    """
    Receive incoming WhatsApp messages from Twilio.
    Twilio sends form-encoded POST data (not JSON).
    """
    # Twilio sends form data, not JSON
    body    = request.form.get("Body", "").strip()
    sender  = request.form.get("From", "")   # format: "whatsapp:+919876543210"
    num_media = request.form.get("NumMedia", "0")

    logger.info("📥 Twilio webhook — From=%s Body=[%s] NumMedia=%s", sender, body, num_media)

    if not sender or not body:
        logger.warning("⚠️ Missing From or Body — ignoring")
        return "", 200

    # Strip "whatsapp:+" prefix to get plain phone number
    phone = sender.replace("whatsapp:+", "").replace("whatsapp:", "").lstrip("+")
    logger.info("📱 Normalised phone: %s", phone)

    try:
        _process_message(phone, body)
    except Exception:
        logger.exception("💥 Unhandled exception in _process_message")

    # Twilio expects empty 200 response (we send replies via API, not TwiML)
    return "", 200


# ===================================================================
#  MESSAGE PROCESSING STATE MACHINE
# ===================================================================

def _process_message(phone: str, text: str) -> None:
    """
    Core conversation state machine.

    States:
        (no session)  → greet & ask for Ullas ID / phone
        awaiting_id   → look up student → show menu
        menu          → route to query handler
    """
    text_lower = text.lower()
    logger.info("🔄 Processing — phone=%s state=? text=[%s]", phone, text)

    # ----- Reset keywords -----
    if text_lower in ("hi", "hello", "hey", "start", "reset"):
        logger.info("🔁 Reset keyword for %s — clearing session", phone)
        clear_session(phone)
        start_session(phone)
        sent = send_message(phone, _WELCOME_MSG)
        logger.info("📤 Welcome sent to %s — success=%s", phone, sent)
        return

    # ----- Get existing session -----
    sess = get_session(phone)
    logger.debug("🗂  Session for %s: %s", phone, sess)

    if sess is None:
        logger.info("🆕 No session for %s — creating new", phone)
        start_session(phone)
        sent = send_message(phone, _WELCOME_MSG)
        logger.info("📤 Welcome sent to %s — success=%s", phone, sent)
        return

    state = sess.get("state", "awaiting_id")
    logger.info("📍 State for %s: %s", phone, state)

    # ----- State: awaiting_id -----
    if state == "awaiting_id":
        logger.info("🔍 Looking up student: [%s]", text)
        ullas_id = lookup_student(text)
        logger.info("🔍 Lookup result: %s", ullas_id)

        if ullas_id is None:
            logger.warning("❌ Student not found for [%s] from %s", text, phone)
            sent = send_message(
                phone,
                "❌ We could not find a student with that ID or phone number.\n"
                "Please check and try again.\n\n"
                "🆔 *Ullas ID* format: UL-XX-YYYY-NNNNN\n"
                "📱 *Phone* format: 91XXXXXXXXXX",
            )
            logger.info("📤 Not-found message sent — success=%s", sent)
            return

        logger.info("✅ Student found: %s", ullas_id)
        sess["ullas_id"] = ullas_id
        sess["state"]    = "menu"
        touch_session(phone)
        sent = send_message(phone, f"✅ Student found: *{ullas_id}*\n\n{MAIN_MENU}")
        logger.info("📤 Menu sent after login — success=%s", sent)
        return

    # ----- State: menu -----
    if state == "menu":
        touch_session(phone)

        if text_lower in ("menu", "back", "main menu", "0"):
            logger.info("🏠 Menu keyword from %s", phone)
            send_message(phone, MAIN_MENU)
            return

        if text_lower in ("exit", "quit", "logout", "bye"):
            logger.info("🚪 Logout from %s", phone)
            clear_session(phone)
            send_message(phone, "👋 You have been logged out.\nSend *Hi* anytime to start again.")
            return

        if text in MENU_HANDLERS:
            label, handler = MENU_HANDLERS[text]
            ullas_id = sess.get("ullas_id")
            logger.info("📋 Option %s (%s) by %s (ullas_id=%s)", text, label, phone, ullas_id)
            try:
                response = handler(ullas_id)
                logger.debug("📋 Handler response: %s", response[:100])
            except Exception:
                logger.exception("💥 Handler for option %s raised an exception", text)
                response = "⚠️ An error occurred. Please try again."
            sent = send_message(phone, f"📋 *{label}*\n\n{response}\n\n_Reply *menu* to go back._")
            logger.info("📤 Handler response sent — success=%s", sent)
            return

        if text == "7":
            logger.info("📞 Support option by %s", phone)
            send_message(phone, talk_to_support())
            return

        logger.warning("🤔 Unrecognised input [%s] from %s in menu state", text, phone)
        send_message(phone, "🤔 I didn't understand that.\n\n" + MAIN_MENU)
        return

    # ----- Fallback -----
    logger.error("💥 Unknown state [%s] for %s — resetting", state, phone)
    clear_session(phone)
    send_message(phone, "Something went wrong. Please send *Hi* to restart.")


# ===================================================================
#  ENTRY POINT
# ===================================================================

if __name__ == "__main__":
    logger.info("🚀 Starting Flask dev server on port %s", FLASK_PORT)
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
