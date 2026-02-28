"""
Ullas Student WhatsApp Chatbot — Flask Middleware
=================================================
Entry point. Handles WhatsApp webhook verification & incoming messages.
Routes messages through authentication → menu → query handlers.
"""
import logging
import sys
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

# ---- Logging — stream to stdout so Render captures it ----
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)

# Log startup info immediately so Render shows it on boot
logger.info("=" * 60)
logger.info("🚀  Ullas WhatsApp Chatbot — starting up")
logger.info("    FLASK_PORT   : %s", FLASK_PORT)
logger.info("    FLASK_DEBUG  : %s", FLASK_DEBUG)
logger.info("    VERIFY_TOKEN : %s", VERIFY_TOKEN[:6] + "***" if VERIFY_TOKEN else "NOT SET")
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


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """
    Meta webhook verification (hub.challenge handshake).
    Called once when you register the webhook URL in Meta dashboard.
    """
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    logger.info("🔐 /webhook GET — mode=%s token=%s challenge=%s", mode, token, challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("✅ Webhook verified successfully")
        return challenge, 200

    logger.warning(
        "❌ Webhook verification FAILED — "
        "expected token=%s but got token=%s, mode=%s",
        VERIFY_TOKEN, token, mode
    )
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def handle_message():
    """
    Receive incoming WhatsApp messages and route them through the
    authentication → menu → query handler pipeline.
    """
    raw = request.get_data(as_text=True)
    logger.debug("📥 /webhook POST raw body: %s", raw[:500])  # first 500 chars

    data = request.get_json(silent=True)
    if data is None:
        logger.warning("⚠️ /webhook POST — could not parse JSON body, ignoring")
        return jsonify({"status": "ignored"}), 200

    try:
        entries = data.get("entry", [])
        logger.debug("📦 Payload has %d entries", len(entries))

        for entry in entries:
            changes = entry.get("changes", [])
            logger.debug("   Entry has %d changes", len(changes))

            for change in changes:
                value    = change.get("value", {})
                messages = value.get("messages", [])
                logger.debug("   Change has %d messages", len(messages))

                for msg in messages:
                    msg_type = msg.get("type")
                    logger.debug("   Message type: %s", msg_type)

                    if msg_type == "text":
                        phone = msg["from"]
                        text  = msg["text"]["body"].strip()
                        logger.info("📩 Received text from %s: [%s]", phone, text)
                        _process_message(phone, text)
                    else:
                        logger.info("ℹ️ Skipping non-text message type: %s", msg_type)

    except Exception:
        logger.exception("💥 Unhandled exception processing webhook payload")

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
    logger.info("🔄 Processing message — phone=%s text=[%s] lower=[%s]", phone, text, text_lower)

    # ----- Reset keywords — always restart regardless of session state -----
    if text_lower in ("hi", "hello", "hey", "start", "reset"):
        logger.info("🔁 Reset keyword detected for %s — clearing session", phone)
        clear_session(phone)
        start_session(phone)
        sent = send_message(phone, _WELCOME_MSG)
        logger.info("📤 Welcome message sent to %s — success=%s", phone, sent)
        return

    # ----- Get existing session -----
    sess = get_session(phone)
    logger.debug("🗂  Session for %s: %s", phone, sess)

    if sess is None:
        logger.info("🆕 No session found for %s — creating new session", phone)
        start_session(phone)
        sent = send_message(phone, _WELCOME_MSG)
        logger.info("📤 Welcome message sent to %s — success=%s", phone, sent)
        return

    state = sess.get("state", "awaiting_id")
    logger.info("📍 Session state for %s: %s", phone, state)

    # ----- State: awaiting_id -----
    if state == "awaiting_id":
        logger.info("🔍 Looking up student with identifier: [%s]", text)
        ullas_id = lookup_student(text)
        logger.info("🔍 Lookup result for [%s]: %s", text, ullas_id)

        if ullas_id is None:
            logger.warning("❌ Student not found for identifier [%s] from %s", text, phone)
            sent = send_message(
                phone,
                "❌ We could not find a student with that ID or phone number.\n"
                "Please check and try again.\n\n"
                "🆔 *Ullas ID* format: UL-XX-YYYY-NNNNN\n"
                "📱 *Phone* format: 91XXXXXXXXXX",
            )
            logger.info("📤 Not-found message sent to %s — success=%s", phone, sent)
            return

        logger.info("✅ Student found — ullas_id=%s for phone=%s", ullas_id, phone)
        sess["ullas_id"] = ullas_id
        sess["state"]    = "menu"
        touch_session(phone)
        sent = send_message(phone, f"✅ Student found: *{ullas_id}*\n\n{MAIN_MENU}")
        logger.info("📤 Menu sent to %s after login — success=%s", phone, sent)
        return

    # ----- State: menu -----
    if state == "menu":
        touch_session(phone)

        # Navigation keywords
        if text_lower in ("menu", "back", "main menu", "0"):
            logger.info("🏠 Menu keyword from %s — resending main menu", phone)
            send_message(phone, MAIN_MENU)
            return

        # Logout keywords
        if text_lower in ("exit", "quit", "logout", "bye"):
            logger.info("🚪 Logout keyword from %s — clearing session", phone)
            clear_session(phone)
            send_message(phone, "👋 You have been logged out.\nSend *Hi* anytime to start again.")
            return

        # Numbered menu options 1–6
        if text in MENU_HANDLERS:
            label, handler = MENU_HANDLERS[text]
            ullas_id = sess.get("ullas_id")
            logger.info("📋 Menu option %s (%s) selected by %s (ullas_id=%s)", text, label, phone, ullas_id)
            try:
                response = handler(ullas_id)
                logger.debug("📋 Handler response for option %s: %s", text, response[:100])
            except Exception:
                logger.exception("💥 Handler for option %s raised an exception", text)
                response = "⚠️ An error occurred. Please try again or contact support."
            sent = send_message(phone, f"📋 *{label}*\n\n{response}\n\n_Reply *menu* to go back._")
            logger.info("📤 Handler response sent to %s — success=%s", phone, sent)
            return

        # Option 7 — Talk to Support
        if text == "7":
            logger.info("📞 Support option selected by %s", phone)
            sent = send_message(phone, talk_to_support())
            logger.info("📤 Support info sent to %s — success=%s", phone, sent)
            return

        # Unrecognised input
        logger.warning("🤔 Unrecognised input [%s] from %s in menu state", text, phone)
        send_message(phone, "🤔 I didn't understand that.\n\n" + MAIN_MENU)
        return

    # ----- Fallback: unknown / corrupt state -----
    logger.error("💥 Unknown session state [%s] for %s — resetting session", state, phone)
    clear_session(phone)
    send_message(phone, "Something went wrong. Please send *Hi* to restart.")


# ===================================================================
#  ENTRY POINT
# ===================================================================

if __name__ == "__main__":
    logger.info("🚀 Starting Flask dev server on port %s", FLASK_PORT)
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)
