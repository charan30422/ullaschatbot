"""
Query handlers for the Ullas WhatsApp Chatbot.
"""

_DIV = "─────────────────────────"
_NAV = "↩️ Reply *menu* for Main Menu"

MAIN_MENU = (
    "🌟 *Ullas Student Support* 🌟\n\n"
    "Please choose an option:\n\n"
    "1️⃣  What is my Registration Status?\n"
    "2️⃣  Where is my UEE Exam Centre?\n"
    "3️⃣  What is my Attendance & Eligibility?\n"
    "4️⃣  What is my Scholarship Status?\n"
    "5️⃣  Can I get my Certificate?\n"
    "6️⃣  Am I marked for Renewal?\n"
    "7️⃣  Ask Ullas\n"
    "8️⃣  FAQs\n\n"
    "_Reply with a number (1–8)_"
)


def get_registration_status() -> str:
    """1️⃣ Registration Status"""
    return (
        "❓ *What is my Registration Status?*\n"
        f"{_DIV}\n\n"
        "✅ *Status:* VERIFIED\n"
        "📅 *Verified on:* 12 July 2026\n"
        "🏫 *School:* GoveGovt Hss School \n\n"
        f"{_DIV}\n"
        "🎓 You are eligible for the *UEE Exam*\n"
        "📆 *Exam Date:* 12 March 2026\n\n"
        f"{_NAV}"
    )


def get_exam_centre() -> str:
    """2️⃣ UEE Exam Centre Details"""
    return (
        "❓ *Where is my UEE Exam Centre?*\n"
        f"{_DIV}\n\n"
        "📍 *Centre:* St. Mary's High School\n"
        "📌 *Location:* Andheri East, Mumbai\n"
        "🗓  *Exam Date:* 12 March 2026\n"
        "🕘 *Reporting Time:* 8:30 AM\n\n"
        "⚠️ Carry your School ID Card and reach\n"
        "the centre *30 minutes* before reporting time.\n\n"
        "🗺  *View on Map:*\n"
        "https://maps.google.com/?q=St.+Mary's+High+School,+Andheri+East\n\n"
        f"{_NAV}"
    )


def get_attendance() -> str:
    """3️⃣ Attendance & Eligibility"""
    return (
        "❓ *What is my Attendance & Eligibility?*\n"
        f"{_DIV}\n\n"
        "📅 *Summit 1:* 15 Jan 2026\n"
        "✅ Present | Attendance: 80%\n"
        "🎯 Eligible for Scholarship\n\n"
        f"{_DIV}\n"
        "📅 *Summit 2:* 20 Feb 2026\n"
        "❌ Absent | Attendance: 55%\n"
        "⛔ Not eligible for Scholarship\n\n"
        f"{_DIV}\n"
        "📅 *Summit 3:* ─ Not Applicable\n"
        "📅 *Summit 4:* ─ Not Applicable\n\n"
        f"{_DIV}\n"
        "📈 *Total Attendance:* 67%\n\n"
        f"{_NAV}"
    )


def get_scholarship_status() -> str:
    """4️⃣ Scholarship Status"""
    return (
        "❓ *What is my Scholarship Status?*\n"
        f"{_DIV}\n\n"
        "✅ *Summit 1 Scholarship:* DISBURSED\n"
        "   💵 Amount: ₹900\n"
        "   📅 Date: 14 August 2026\n"
        "   🏦 Bank: SBI XXXX\n"
        "   📤 Transfer: Successful\n\n"
        f"{_DIV}\n"
        "⏳ *Summit 2 Scholarship:* PENDING\n"
        "   📝 Awaiting attendance validation\n\n"
        f"{_NAV}"
    )


def get_certificate_status() -> str:
    """5️⃣ Certificate Status"""
    return (
        "❓ *Can I get my Certificate?*\n"
        f"{_DIV}\n\n"
        "✅ *Status:* Available\n"
        "📜 *Type:* Participation Certificate\n"
        "🌟 *Event:* Summit1\n\n"
        "⬇️ *Download Certificate (PDF):*\n"
        "https://ullas.example.com/cert/download\n\n"
        f"{_NAV}"
    )


def get_renewal_status() -> str:
    """6️⃣ Renewal Status"""
    return (
        "❓ *Am I marked for Renewal?*\n"
        f"{_DIV}\n\n"
        "✅ Renewal confirmed for this year! 🎉\n\n"
        "👤 *Category:* Renewal\n"
        "📚 *Current Class:* 11\n"
        "📅 *Batch Year:* 2024\n\n"
        f"{_NAV}"
    )


def ask_ullas() -> str:
    """7️⃣ Ask Ullas"""
    return (
        "🤖 *Ask Ullas*\n"
        f"{_DIV}\n\n"
        "Hi! I'm Ullas Bot. Here are some things\n"
        "I can answer right away:\n\n"
        "💬 *Common Questions:*\n\n"
        "🔹 *What is Ullas?*\n"
        "Ullas is a scholarship & skilling program\n"
        "by the Government of India for students.\n\n"
        "🔹 *When does the program run?*\n"
        "The program runs annually. Enrolment\n"
        "begins every academic year in April.\n\n"
        "🔹 *Who can apply?*\n"
        "Students from Class 9–12 in government\n"
        "and aided schools are eligible.\n\n"
        "🔹 *How do I check my status?*\n"
        "Use options 1–6 in the main menu.\n\n"
        f"{_DIV}\n"
        "For more queries, reach us at:\n"
        "📧 support@ullas.example.com\n\n"
        f"{_NAV}"
    )


def get_faqs() -> str:
    """8️⃣ FAQs"""
    return (
        "📋 *Frequently Asked Questions*\n"
        f"{_DIV}\n\n"
        "*Q1. What documents are needed?*\n"
        "📄 Aadhaar card, School ID, Bank passbook\n"
        "   (parent/student), and a recent photo.\n\n"
        f"{_DIV}\n"
        "*Q2. When is the scholarship paid?*\n"
        "💰 1st instalment after registration\n"
        "   verification. 2nd after 60% attendance.\n\n"
        f"{_DIV}\n"
        "*Q3. What is the UEE exam?*\n"
        "📝 Unified Eligibility Exam — conducted to\n"
        "   assess student eligibility for the program.\n\n"
        f"{_DIV}\n"
        "*Q4. I lost my certificate. What to do?*\n"
        "🎓 Re-download from the portal link in\n"
        "   option 5, or contact support.\n\n"
        f"{_DIV}\n"
        "*Q5. My bank transfer failed. Now what?*\n"
        "🏦 Update your bank details in the app\n"
        "   and contact your school SPOC.\n\n"
        f"{_NAV}"
    )


def talk_to_support() -> str:
    """9️⃣ Talk to Support"""
    return (
        "📞 *Ullas Support*\n"
        f"{_DIV}\n\n"
        "Thanks for reaching out to Ullas Support 🙏\n\n"
        "📧 *Email:* support@ullas.example.com\n"
        "📱 *Helpline:* 1800-XXX-XXXX _(Toll-free)_\n"
        "🕘 *Hours:* Mon–Sat, 9 AM – 6 PM\n\n"
        "Contact the *Ullas Support Team* for\n"
        "any further assistance.\n\n"
        f"{_NAV}"
    )


# Map menu option number → (label, handler function)
MENU_HANDLERS = {
    "1": ("Registration Status",      get_registration_status),
    "2": ("UEE Exam Centre Details",  get_exam_centre),
    "3": ("Attendance & Eligibility", get_attendance),
    "4": ("Scholarship Status",       get_scholarship_status),
    "5": ("Certificate Status",       get_certificate_status),
    "6": ("Renewal Status",           get_renewal_status),
    "7": ("Ask Ullas",                ask_ullas),
    "8": ("FAQs",                     get_faqs),
}
