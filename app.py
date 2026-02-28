"""
Ullas Student WhatsApp Chatbot — Flask Middleware
=================================================
Entry point. Handles WhatsApp webhook verification & incoming messages.
Routes messages through authentication → menu → query handlers.
"""
import logging
from flask import Flask, request, jsonify

from config import VERIFY_TOKEN, FLASK_PORT, FLASK_DEBUG
from auth import (
    get_session,
    start_session,
    lookup_student,
    touch_session,
    clear_session,
)
from handlers import MAIN_MENU, MENU_HANDLERS, talk_to_support
from whatsapp import send_message

# ---- Logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

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
    return jsonify({"status": "ok", "service": "ullas-whatsapp-chatbot"})


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """
    Meta webhook verification (hub.challenge handshake).
    Called once when you register the webhook URL in Meta dashboard.
    """
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("✅ Webhook verified successfully")
        return challenge, 200

    logger.warning("❌ Webhook verification failed — bad token or mode")
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def handle_message():
    """
    Receive incoming WhatsApp messages and route them through the
    authentication → menu → query handler pipeline.
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"status": "ignored"}), 200

    try:
        entries = data.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value    = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    if msg.get("type") == "text":
                        phone = msg["from"]
                        text  = msg["text"]["body"].strip()
                        logger.info("📩 From %s: %s", phone, text)
                        _process_message(phone, text)
    except Exception:
        logger.exception("Error processing webhook payload")

    # Always return 200 so Meta does not retry
    return jsonify({"status": "received"}), 200


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

    # ----- Reset keywords — always restart regardless of session state -----
    if text_lower in ("hi", "hello", "hey", "start", "reset"):
        clear_session(phone)
        start_session(phone)
        send_message(phone, _WELCOME_MSG)
        return

    # ----- Get existing session -----
    sess = get_session(phone)
    if sess is None:
        # No session exists — create one and ask for ID
        start_session(phone)
        send_message(phone, _WELCOME_MSG)
        return

    state = sess.get("state", "awaiting_id")

    # ----- State: awaiting_id -----
    if state == "awaiting_id":
        ullas_id = lookup_student(text)
        if ullas_id is None:
            send_message(
                phone,
                "❌ We could not find a student with that ID or phone number.\n"
                "Please check and try again.\n\n"
                "🆔 *Ullas ID* format: UL-XX-YYYY-NNNNN\n"
                "📱 *Phone* format: 91XXXXXXXXXX",
            )
            return

        sess["ullas_id"] = ullas_id
        sess["state"]    = "menu"
        touch_session(phone)
        send_message(phone, f"✅ Student found: *{ullas_id}*\n\n{MAIN_MENU}")
        return

    # ----- State: menu -----
    if state == "menu":
        touch_session(phone)

        # Navigation keywords
        if text_lower in ("menu", "back", "main menu", "0"):
            send_message(phone, MAIN_MENU)
            return

        # Logout keywords
        if text_lower in ("exit", "quit", "logout", "bye"):
            clear_session(phone)
            send_message(phone, "👋 You have been logged out.\nSend *Hi* anytime to start again.")
            return

        # Numbered menu options 1–6
        if text in MENU_HANDLERS:
            label, handler = MENU_HANDLERS[text]
            ullas_id = sess.get("ullas_id")
            response = handler(ullas_id)
            send_message(phone, f"📋 *{label}*\n\n{response}\n\n_Reply *menu* to go back._")
            return

        # Option 7 — Talk to Support
        if text == "7":
            send_message(phone, talk_to_support())
            return

        # Unrecognised input
        send_message(phone, "🤔 I didn't understand that.\n\n" + MAIN_MENU)
        return

    # ----- Fallback: unknown / corrupt state -----
    logger.warning("Unknown session state '%s' for %s — resetting", state, phone)
    clear_session(phone)
    send_message(phone, "Something went wrong. Please send *Hi* to restart.")


# ===================================================================
#  ENTRY POINT
# ===================================================================

if __name__ == "__main__":
    logger.info("🚀 Starting on port %s", FLASK_PORT)
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
