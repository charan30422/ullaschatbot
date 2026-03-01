"""
Ullas WhatsApp Chatbot — Simple Q&A Bot (Twilio)
=================================================
Receives messages via Twilio webhook and replies with
predefined answers for common Ullas student queries.
"""
import os
import logging
import sys
from flask import Flask, request
from twilio.rest import Client

# ---- Logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    stream=sys.stdout,
    force=True,
)
logger = logging.getLogger(__name__)

# ---- Config ----
from dotenv import load_dotenv
load_dotenv()

TWILIO_ACCOUNT_SID     = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN      = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
FLASK_PORT             = int(os.environ.get("PORT", os.environ.get("FLASK_PORT", "10000")))

logger.info("🚀 Ullas WhatsApp Chatbot starting...")
logger.info("   TWILIO_ACCOUNT_SID : %s", TWILIO_ACCOUNT_SID[:6] + "***" if TWILIO_ACCOUNT_SID else "NOT SET")
logger.info("   TWILIO_FROM        : %s", TWILIO_WHATSAPP_NUMBER)
logger.info("   PORT               : %s", FLASK_PORT)

app = Flask(__name__)


# ==============================
# Health Check
# ==============================
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "ullas-chatbot"}, 200


@app.route("/")
def home():
    return "Ullas WhatsApp Chatbot is Running 🚀"


# ==============================
# Twilio Webhook (POST)
# ==============================
@app.route("/webhook", methods=["POST"])
def receive_message():
    sender  = request.form.get("From", "")   # e.g. whatsapp:+918125930620
    body    = request.form.get("Body", "").strip()

    logger.info("📩 From=%s Body=[%s]", sender, body)

    if not sender or not body:
        return "", 200

    # Normalize phone number
    phone = sender.replace("whatsapp:+", "").replace("whatsapp:", "").lstrip("+")

    reply = generate_reply(body)
    logger.info("💬 Reply → %s", reply[:80])

    send_message(phone, reply)
    return "", 200


# ==============================
# Chatbot Logic — Q&A
# ==============================
MENU = (
    "Welcome to Ullas Support 🌟\n\n"
    "Please choose an option:\n\n"
    "1️⃣ When is the UEE exam?\n"
    "2️⃣ Exam centre details\n"
    "3️⃣ Registration status\n"
    "4️⃣ Attendance\n"
    "5️⃣ Scholarship status\n"
    "6️⃣ Certificate status\n"
    "7️⃣ Renewal status\n\n"
    "Reply with the number (1-7)."
)

def generate_reply(user_text: str) -> str:
    text = user_text.lower().strip()

    if text in ["hi", "hello", "hey", "start", "menu"]:
        return MENU

    elif text == "1":
        return (
            "📅 *UEE Exam Date*\n\n"
            "The UEE (Ullas Eligibility Exam) date will be announced "
            "on the official Ullas portal and communicated to registered students.\n\n"
            "📌 Check: ullas.gov.in\n\n"
            "_Reply *menu* to go back._"
        )

    elif text == "2":
        return (
            "🏫 *Exam Centre Details*\n\n"
            "Your exam centre will be allotted based on your district "
            "and communicated via your registered email and the student portal.\n\n"
            "📌 Login to the portal to check your allotted centre.\n\n"
            "_Reply *menu* to go back._"
        )

    elif text == "3":
        return (
            "📋 *Registration Status*\n\n"
            "You can check your registration status by:\n"
            "1. Logging into the Ullas student portal\n"
            "2. Going to 'My Profile' → 'Registration Status'\n\n"
            "📌 If status shows REJECTED, re-upload the required documents.\n\n"
            "_Reply *menu* to go back._"
        )

    elif text == "4":
        return (
            "📊 *Attendance*\n\n"
            "Minimum *75% attendance* is required across all summits "
            "to be eligible for the 2nd scholarship installment.\n\n"
            "Summit sessions:\n"
            "• Summit 1 • Summit 2 • Summit 3 • Summit 4\n\n"
            "📌 Check your attendance in the student portal.\n\n"
            "_Reply *menu* to go back._"
        )

    elif text == "5":
        return (
            "💰 *Scholarship Status*\n\n"
            "The Ullas scholarship is disbursed in 2 installments:\n"
            "• *1st installment* — after registration verification\n"
            "• *2nd installment* — after 75% summit attendance\n\n"
            "📌 Check payment status in the portal under 'Scholarship'.\n"
            "If payment failed, update your bank details.\n\n"
            "_Reply *menu* to go back._"
        )

    elif text == "6":
        return (
            "🎓 *Certificate Status*\n\n"
            "Participation certificates are issued after the final summit.\n\n"
            "📌 Download from the portal under 'My Certificates'.\n"
            "If not available, contact your school SPOC.\n\n"
            "_Reply *menu* to go back._"
        )

    elif text == "7":
        return (
            "🔄 *Renewal Status*\n\n"
            "Existing Ullas students must renew each academic year.\n\n"
            "📌 Log into the portal and go to 'Renewal' section.\n"
            "Contact your school SPOC if renewal is pending.\n\n"
            "_Reply *menu* to go back._"
        )

    else:
        return (
            "🤔 I didn't understand that.\n\n"
            "Please type *Hi* to see the main menu or choose 1-7."
        )


# ==============================
# Send Message via Twilio
# ==============================
def send_message(to: str, body: str) -> None:
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        to_formatted = f"whatsapp:+{to.lstrip('+')}"

        raw_from = TWILIO_WHATSAPP_NUMBER.strip()
        if raw_from.startswith("whatsapp:"):
            from_formatted = raw_from
        elif raw_from.startswith("+"):
            from_formatted = f"whatsapp:{raw_from}"
        else:
            from_formatted = f"whatsapp:+{raw_from}"

        logger.info("📤 Sending to %s from %s", to_formatted, from_formatted)

        msg = client.messages.create(
            body=body,
            from_=from_formatted,
            to=to_formatted,
        )
        logger.info("✅ Sent! SID=%s status=%s", msg.sid, msg.status)

    except Exception as exc:
        logger.error("❌ Twilio error: %s", exc)


# ==============================
# Entry Point
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=False)
