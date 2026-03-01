"""
Query handlers for the Ullas WhatsApp Chatbot.
Each function takes an ullas_id, looks up mock data, and returns
a richly formatted WhatsApp-friendly response string.
"""
from mock_data import (
    REGISTRATION,
    EXAM_CENTRES,
    ATTENDANCE,
    SCHOLARSHIP,
    CERTIFICATES,
    RENEWAL,
)

# Divider line used across all responses
_DIV = "─────────────────────────"
_NAV = "_Reply *menu* to go back to Main Menu_"

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


def get_registration_status(ullas_id: str) -> str:
    """1️⃣ Registration Status"""
    reg = REGISTRATION.get(ullas_id)
    if reg is None:
        return (
            "📋 *REGISTRATION STATUS*\n"
            f"{_DIV}\n"
            "⚠️ No registration record found for your account.\n"
            "Please contact your school SPOC.\n\n"
            f"{_NAV}"
        )

    if reg["status"] == "VERIFIED":
        return (
            "╔══════════════════════════╗\n"
            "  ✅ *REGISTRATION STATUS*\n"
            "╚══════════════════════════╝\n\n"
            f"🆔 *Ullas ID:* {ullas_id}\n"
            f"📅 *Verified on:* {reg['verified_on']}\n"
            f"🎉 *Status:* VERIFIED\n\n"
            f"{_DIV}\n"
            f"🏆 Congratulations! You are eligible for:\n"
            f"*{reg['eligible_for']}*\n\n"
            f"🌐 *Workshop Portal:*\n"
            f"https://workshop.ullas.example.com\n\n"
            f"{_NAV}"
        )
    return (
        "╔══════════════════════════╗\n"
        "  ❌ *REGISTRATION STATUS*\n"
        "╚══════════════════════════╝\n\n"
        f"🆔 *Ullas ID:* {ullas_id}\n"
        f"📌 *Status:* {reg['status']}\n\n"
        f"{_DIV}\n"
        f"📝 *Reason:* {reg.get('reason', 'N/A')}\n"
        f"👉 *Action:* {reg.get('action', 'Please contact support.')}\n\n"
        f"{_NAV}"
    )


def get_exam_centre(ullas_id: str) -> str:
    """2️⃣ Exam Centre Details"""
    centre = EXAM_CENTRES.get(ullas_id)
    if centre is None:
        return (
            "🏫 *EXAM CENTRE DETAILS*\n"
            f"{_DIV}\n"
            "⚠️ No exam centre information found for your account.\n\n"
            f"{_NAV}"
        )

    if centre.get("allocated"):
        name = centre['centre_name']
        loc  = centre['location']
        maps_url = f"https://maps.google.com/?q={name.replace(' ', '+')},+{loc.replace(' ', '+')}"
        return (
            "╔══════════════════════════╗\n"
            "  🏫 *EXAM CENTRE DETAILS*\n"
            "╚══════════════════════════╝\n\n"
            f"📍 *Centre:* {name}\n"
            f"📌 *Location:* {loc}\n"
            f"🗓  *Exam Date:* {centre['exam_date']}\n"
            f"🕘 *Reporting Time:* {centre['reporting_time']}\n\n"
            f"{_DIV}\n"
            f"⚠️ Please carry your School ID Card and reach the centre "
            f"30 minutes before the reporting time.\n\n"
            f"🗺  *View on Map:*\n{maps_url}\n\n"
            f"{_NAV}"
        )
    return (
        "╔══════════════════════════╗\n"
        "  🏫 *EXAM CENTRE DETAILS*\n"
        "╚══════════════════════════╝\n\n"
        "⏳ *Centre Not Yet Allocated*\n\n"
        f"{_DIV}\n"
        "Please check again after the centre allocation date.\n\n"
        f"{_NAV}"
    )


def get_attendance(ullas_id: str) -> str:
    """3️⃣ Attendance & Eligibility"""
    att = ATTENDANCE.get(ullas_id)
    if att is None:
        return (
            "📊 *ATTENDANCE SUMMARY*\n"
            f"{_DIV}\n"
            "⚠️ No attendance records found for your account.\n\n"
            f"{_NAV}"
        )

    def mark(val: str) -> str:
        return "✅" if val == "Present" else "❌"

    pct     = att['total_percentage']
    eligible = att['eligible']
    bar     = "🟩" * (pct // 10) + "⬜" * (10 - pct // 10)

    return (
        "╔══════════════════════════╗\n"
        "  📊 *ATTENDANCE SUMMARY*\n"
        "╚══════════════════════════╝\n\n"
        f"Summit 1: {mark(att['summit_1'])} {att['summit_1']}\n"
        f"Summit 2: {mark(att['summit_2'])} {att['summit_2']}\n"
        f"Summit 3: {mark(att['summit_3'])} {att['summit_3']}\n"
        f"Summit 4: {mark(att['summit_4'])} {att['summit_4']}\n\n"
        f"{_DIV}\n"
        f"📈 *TOTAL ATTENDANCE:* {pct}%\n"
        f"{bar}\n\n"
        f"{'🎯' if eligible else '⚠️'} *ELIGIBILITY STATUS:*\n"
        f"{att['eligibility_note']}\n\n"
        f"{_NAV}"
    )


def get_scholarship_status(ullas_id: str) -> str:
    """4️⃣ Scholarship Status"""
    sch = SCHOLARSHIP.get(ullas_id)
    if sch is None:
        return (
            "💰 *SCHOLARSHIP STATUS*\n"
            f"{_DIV}\n"
            "⚠️ No scholarship record found for your account.\n\n"
            f"{_NAV}"
        )

    lines = [
        "╔══════════════════════════╗",
        "  💰 *SCHOLARSHIP STATUS*",
        "╚══════════════════════════╝\n",
    ]

    # First scholarship
    first = sch.get("first", {})
    if first.get("status") == "Processed":
        lines += [
            "✅ *1st Scholarship:* DISBURSED",
            f"   💵 Amount: {first['amount']}",
            f"   📅 Date: {first['date']}",
            f"   🏦 Bank: {first['bank']} XXXX",
            f"   📤 Transfer: {first['transfer_status']}",
        ]
    elif first.get("status") == "Failed":
        lines += [
            "❌ *1st Scholarship:* FAILED",
            f"   📝 Reason: {first.get('reason', 'N/A')}",
            f"   👉 Action: {first.get('action', 'Contact support.')}",
        ]
    else:
        lines += [f"⏳ *1st Scholarship:* {first.get('status', 'N/A')}"]

    lines.append(f"\n{_DIV}")

    # Second scholarship
    second = sch.get("second", {})
    if second.get("status") == "Processed":
        lines += [
            "✅ *2nd Scholarship:* DISBURSED",
            f"   💵 Amount: {second['amount']}",
            f"   📅 Date: {second['date']}",
            f"   🏦 Bank: {second['bank']} XXXX",
            f"   📤 Transfer: {second['transfer_status']}",
        ]
    elif second.get("status") == "Pending":
        lines += [
            "⏳ *2nd Scholarship:* PENDING",
            f"   📝 Reason: {second.get('reason', 'N/A')}",
        ]
    else:
        lines += [f"⏳ *2nd Scholarship:* {second.get('status', 'N/A')}"]

    lines += ["", _NAV]
    return "\n".join(lines)


def get_certificate_status(ullas_id: str) -> str:
    """5️⃣ Certificate Status"""
    cert = CERTIFICATES.get(ullas_id)
    if cert is None:
        return (
            "🎓 *CERTIFICATE STATUS*\n"
            f"{_DIV}\n"
            "⚠️ No certificate record found for your account.\n\n"
            f"{_NAV}"
        )

    if cert.get("available"):
        return (
            "╔══════════════════════════╗\n"
            "  🎓 *CERTIFICATE STATUS*\n"
            "╚══════════════════════════╝\n\n"
            f"✅ *Status:* Available\n"
            f"📜 *Certificate Type:* {cert['type']}\n"
            f"🌟 *Event Name:* {cert['event']}\n\n"
            f"{_DIV}\n"
            f"⬇️ *Download Certificate (PDF):*\n"
            f"{cert['download_link']}\n\n"
            f"{_NAV}"
        )
    return (
        "╔══════════════════════════╗\n"
        "  🎓 *CERTIFICATE STATUS*\n"
        "╚══════════════════════════╝\n\n"
        f"❌ *Status:* Not Available\n\n"
        f"{_DIV}\n"
        f"📝 *Reason:* {cert.get('reason', 'N/A')}\n\n"
        f"{_NAV}"
    )


def get_renewal_status(ullas_id: str) -> str:
    """6️⃣ Renewal Status"""
    ren = RENEWAL.get(ullas_id)
    if ren is None:
        return (
            "╔══════════════════════════╗\n"
            "  🔄 *RENEWAL STATUS*\n"
            "╚══════════════════════════╝\n\n"
            "⚠️ No renewal record found.\n"
            "Please contact your school SPOC.\n\n"
            f"{_NAV}"
        )
    return (
        "╔══════════════════════════╗\n"
        "  🔄 *RENEWAL STATUS*\n"
        "╚══════════════════════════╝\n\n"
        f"✅ *Renewal confirmed for next academic year!*\n\n"
        f"{_DIV}\n"
        f"👤 *Student Category:* {ren['category']}\n"
        f"📚 *Current Class:* {ren['current_class']}\n"
        f"📅 *Batch Year:* {ren['batch_year']}\n\n"
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
        "📱 *Helpline:* 1800-XXX-XXXX _(Toll-free)_\n"
        "🕘 *Hours:* Mon–Sat, 9 AM – 6 PM\n\n"
        f"{_DIV}\n"
        "An agent will get back to you shortly.\n\n"
        f"{_NAV}"
    )


# Map menu option number → (label, handler function)
MENU_HANDLERS = {
    "1": ("Registration Status",           get_registration_status),
    "2": ("UEE Exam Centre Details",        get_exam_centre),
    "3": ("Attendance & Eligibility",       get_attendance),
    "4": ("Scholarship Status",             get_scholarship_status),
    "5": ("Certificate Status",             get_certificate_status),
    "6": ("Renewal Status",                 get_renewal_status),
}
