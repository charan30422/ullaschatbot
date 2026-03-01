"""
Query handlers for the Ullas WhatsApp Chatbot.
Each function returns a formatted WhatsApp-friendly response string.
No Ullas ID required — responses are informative and generic.
"""

# Divider line used across all responses
_DIV = "─────────────────────────"
_NAV = "↩️ Reply *menu* for Main Menu"

MAIN_MENU = (
    "╔══════════════════════════╗\n"
    "  🌟 *Ullas Student Support* 🌟\n"
    "╚══════════════════════════╝\n\n"
    "Please choose an option:\n\n"
    "1️⃣  What is my Registration Status?\n"
    "2️⃣  Where is my UEE Exam Centre?\n"
    "3️⃣  What is my Attendance & Eligibility?\n"
    "4️⃣  What is my Scholarship Status?\n"
    "5️⃣  Can I get my Certificate?\n"
    "6️⃣  Am I marked for Renewal?\n"
    "7️⃣  Talk to Support\n\n"
    "_Reply with a number (1–7)_"
)


def get_registration_status() -> str:
    """1️⃣ Registration Status"""
    return (
        "╔══════════════════════════╗\n"
        "  ✅ *REGISTRATION STATUS*\n"
        "╚══════════════════════════╝\n\n"
        "Your registration has been *VERIFIED* ✅\n\n"
        f"{_DIV}\n"
        "🏆 You are eligible for the:\n"
        "*CAN-DO Workshop*\n\n"
        "🌐 *Workshop Portal:*\n"
        "https://workshop.ullas.example.com\n\n"
        f"{_NAV}"
    )


def get_exam_centre() -> str:
    """2️⃣ UEE Exam Centre Details"""
    return (
        "╔══════════════════════════╗\n"
        "  🏫 *UEE EXAM CENTRE*\n"
        "╚══════════════════════════╝\n\n"
        "📍 *Centre:* St. Mary's High School\n"
        "📌 *Location:* Andheri East, Mumbai\n"
        "🗓  *Exam Date:* 12 March 2026\n"
        "🕘 *Reporting Time:* 8:30 AM\n\n"
        f"{_DIV}\n"
        "⚠️ Please carry your School ID Card\n"
        "and reach the centre *30 minutes* before\n"
        "the reporting time.\n\n"
        "🗺  *View on Map:*\n"
        "https://maps.google.com/?q=St.+Mary's+High+School,+Andheri+East\n\n"
        f"{_NAV}"
    )


def get_attendance() -> str:
    """3️⃣ Attendance & Eligibility"""
    return (
        "╔══════════════════════════╗\n"
        "  📊 *ATTENDANCE SUMMARY*\n"
        "╚══════════════════════════╝\n\n"
        "Summit 1: ✅ Present\n"
        "Summit 2: ✅ Present\n"
        "Summit 3: ❌ Absent\n"
        "Summit 4: ✅ Present\n\n"
        f"{_DIV}\n"
        "📈 *TOTAL ATTENDANCE:* 75%\n"
        "🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜\n\n"
        "🎯 *ELIGIBILITY STATUS:*\n"
        "Eligible for 2nd Scholarship ✅\n\n"
        f"{_NAV}"
    )


def get_scholarship_status() -> str:
    """4️⃣ Scholarship Status"""
    return (
        "╔══════════════════════════╗\n"
        "  💰 *SCHOLARSHIP STATUS*\n"
        "╚══════════════════════════╝\n\n"
        "✅ *1st Scholarship:* DISBURSED\n"
        "   💵 Amount: 50%\n"
        "   📅 Date: 14 August 2026\n"
        "   🏦 Bank: SBI XXXX\n"
        "   📤 Transfer: Successful\n\n"
        f"{_DIV}\n"
        "⏳ *2nd Scholarship:* PENDING\n"
        "   � Reason: Awaiting attendance\n"
        "   validation\n\n"
        f"{_NAV}"
    )


def get_certificate_status() -> str:
    """5️⃣ Certificate Status"""
    return (
        "╔══════════════════════════╗\n"
        "  🎓 *CERTIFICATE STATUS*\n"
        "╚══════════════════════════╝\n\n"
        "✅ *Status:* Available\n"
        "📜 *Type:* Participation Certificate\n"
        "🌟 *Event:* Summit 2026\n\n"
        f"{_DIV}\n"
        "⬇️ *Download Certificate (PDF):*\n"
        "https://ullas.example.com/cert/download\n\n"
        f"{_NAV}"
    )


def get_renewal_status() -> str:
    """6️⃣ Renewal Status"""
    return (
        "╔══════════════════════════╗\n"
        "  🔄 *RENEWAL STATUS*\n"
        "╚══════════════════════════╝\n\n"
        "✅ *Renewal confirmed for next\n"
        "academic year!* 🎉\n\n"
        f"{_DIV}\n"
        "👤 *Category:* Renewal\n"
        "📚 *Current Class:* 11\n"
        "📅 *Batch Year:* 2024\n\n"
        f"{_NAV}"
    )


def talk_to_support() -> str:
    """7️⃣ Talk to Support"""
    return (
        "╔══════════════════════════╗\n"
        "  📞 *ULLAS SUPPORT*\n"
        "╚══════════════════════════╝\n\n"
        "Our team is here to help you! 🤝\n\n"
        f"{_DIV}\n"
        "📧 *Email:* support@ullas.example.com\n"
        "📱 *Helpline:* 1800-XXX-XXXX\n"
        "           _(Toll-free)_\n"
        "🕘 *Hours:* Mon–Sat, 9 AM – 6 PM\n\n"
        f"{_DIV}\n"
        "An agent will get back to you shortly.\n\n"
        f"{_NAV}"
    )


# Map menu option number → (label, handler function)
MENU_HANDLERS = {
    "1": ("Registration Status",     get_registration_status),
    "2": ("UEE Exam Centre Details", get_exam_centre),
    "3": ("Attendance & Eligibility",get_attendance),
    "4": ("Scholarship Status",      get_scholarship_status),
    "5": ("Certificate Status",      get_certificate_status),
    "6": ("Renewal Status",          get_renewal_status),
}
