<<<<<<< HEAD
"""
Query handlers for the Ullas WhatsApp Chatbot.
Each function takes an ullas_id, looks up mock data, and returns
a formatted WhatsApp-friendly response string.
"""
from mock_data import (
    STUDENTS,
    REGISTRATION,
    EXAM_CENTRES,
    ATTENDANCE,
    SCHOLARSHIP,
    CERTIFICATES,
    RENEWAL,
)

MAIN_MENU = (
    "Welcome to Ullas Support! 🌟\n\n"
    "Please choose an option to proceed:\n\n"
    "1️⃣ Registration Status\n"
    "2️⃣ Exam Centre Details\n"
    "3️⃣ Attendance & Eligibility\n"
    "4️⃣ Scholarship Status\n"
    "5️⃣ Certificate Status\n"
    "6️⃣ Renewal Status\n"
    "7️⃣ Talk to Support\n\n"
    "Reply with the option number (1-7)."
)


def get_registration_status(ullas_id: str) -> str:
    """1️⃣ Registration Status"""
    reg = REGISTRATION.get(ullas_id)
    if reg is None:
        return "⚠️ No registration record found for your account."

    if reg["status"] == "VERIFIED":
        return (
            f"✅ *Registration Status:* VERIFIED\n"
            f"📅 Verified on: {reg['verified_on']}\n"
            f"🆔 Ullas ID: {ullas_id}\n\n"
            f"You are eligible for {reg['eligible_for']}."
        )
    else:
        return (
            f"❌ *Registration Status:* {reg['status']}\n"
            f"📝 Reason: {reg.get('reason', 'N/A')}\n"
            f"👉 {reg.get('action', 'Please contact support.')}"
        )


def get_exam_centre(ullas_id: str) -> str:
    """2️⃣ Exam Centre Details"""
    centre = EXAM_CENTRES.get(ullas_id)
    if centre is None:
        return "⚠️ No exam centre information found for your account."

    if centre.get("allocated"):
        return (
            f"🏫 *Exam Centre:* {centre['centre_name']}\n"
            f"📍 Location: {centre['location']}\n"
            f"🕘 Reporting Time: {centre['reporting_time']}\n"
            f"🗓 Exam Date: {centre['exam_date']}"
        )
    else:
        return (
            "⚠️ *Centre Not Yet Allocated*\n"
            "Please check again after the allocation date."
        )


def get_attendance(ullas_id: str) -> str:
    """3️⃣ Attendance & Eligibility"""
    att = ATTENDANCE.get(ullas_id)
    if att is None:
        return "⚠️ No attendance records found for your account."

    status_emoji = "🎯" if att["eligible"] else "⚠️"
    return (
        f"📊 *Attendance Summary:*\n\n"
        f"Summit 1: {att['summit_1']}\n"
        f"Summit 2: {att['summit_2']}\n"
        f"Summit 3: {att['summit_3']}\n"
        f"Summit 4: {att['summit_4']}\n\n"
        f"📈 Total Attendance: {att['total_percentage']}%\n\n"
        f"{status_emoji} *Eligibility Status:* {att['eligibility_note']}"
    )


def get_scholarship_status(ullas_id: str) -> str:
    """4️⃣ Scholarship Status"""
    sch = SCHOLARSHIP.get(ullas_id)
    if sch is None:
        return "⚠️ No scholarship record found for your account."

    lines = []
    # First scholarship
    first = sch.get("first", {})
    if first.get("status") == "Processed":
        lines.append(
            f"💰 *1st Scholarship ({first['amount']}):* Processed\n"
            f"📅 Date: {first['date']}\n"
            f"🏦 Bank: {first['bank']}\n"
            f"✅ Status: {first['transfer_status']}"
        )
    elif first.get("status") == "Failed":
        lines.append(
            f"❌ *1st Scholarship:* Payment Failed\n"
            f"📝 Reason: {first.get('reason', 'N/A')}\n"
            f"👉 {first.get('action', 'Contact support.')}"
        )
    else:
        lines.append(f"⏳ *1st Scholarship:* {first.get('status', 'N/A')}")

    lines.append("")  # blank line

    # Second scholarship
    second = sch.get("second", {})
    if second.get("status") == "Processed":
        lines.append(
            f"💰 *2nd Scholarship ({second['amount']}):* Processed\n"
            f"📅 Date: {second['date']}\n"
            f"🏦 Bank: {second['bank']}\n"
            f"✅ Status: {second['transfer_status']}"
        )
    elif second.get("status") == "Pending":
        lines.append(
            f"⏳ *2nd Scholarship:* Pending\n"
            f"📝 Reason: {second.get('reason', 'N/A')}"
        )
    else:
        lines.append(f"⏳ *2nd Scholarship:* {second.get('status', 'N/A')}")

    return "\n".join(lines)


def get_certificate_status(ullas_id: str) -> str:
    """5️⃣ Certificate Status"""
    cert = CERTIFICATES.get(ullas_id)
    if cert is None:
        return "⚠️ No certificate record found for your account."

    if cert.get("available"):
        return (
            f"🎓 *{cert['type']}:* Available\n"
            f"📅 Event: {cert['event']}\n"
            f"🔗 Download Link: {cert['download_link']}"
        )
    else:
        return (
            f"❌ *Certificate Not Available*\n"
            f"📝 Reason: {cert.get('reason', 'N/A')}"
        )


def get_renewal_status(ullas_id: str) -> str:
    """6️⃣ Renewal Status"""
    ren = RENEWAL.get(ullas_id)
    if ren is None:
        return (
            "⚠️ *No Renewal Record Found*\n"
            "Please contact your school SPOC."
        )

    return (
        f"🔄 *Student Category:* {ren['category']}\n"
        f"📚 Class: {ren['current_class']}\n"
        f"🎓 Batch Year: {ren['batch_year']}"
    )


def talk_to_support() -> str:
    """7️⃣ Talk to Support"""
    return (
        "📞 *Ullas Support*\n\n"
        "You can reach our support team via:\n"
        "📧 Email: support@ullas.example.com\n"
        "📱 Helpline: 1800-XXX-XXXX (Toll-free)\n"
        "🕘 Available: Mon–Sat, 9 AM – 6 PM\n\n"
        "An agent will get back to you shortly."
    )


# Map menu option number → handler
MENU_HANDLERS = {
    "1": ("Registration Status", get_registration_status),
    "2": ("Exam Centre Details", get_exam_centre),
    "3": ("Attendance & Eligibility", get_attendance),
    "4": ("Scholarship Status", get_scholarship_status),
    "5": ("Certificate Status", get_certificate_status),
    "6": ("Renewal Status", get_renewal_status),
}
=======
"""
Query handlers for the Ullas WhatsApp Chatbot.
Each function takes an ullas_id, looks up mock data, and returns
a formatted WhatsApp-friendly response string.
"""
from mock_data import (
    STUDENTS,
    REGISTRATION,
    EXAM_CENTRES,
    ATTENDANCE,
    SCHOLARSHIP,
    CERTIFICATES,
    RENEWAL,
)

MAIN_MENU = (
    "Welcome to Ullas Support! 🌟\n\n"
    "Please choose an option to proceed:\n\n"
    "1️⃣ Registration Status\n"
    "2️⃣ Exam Centre Details\n"
    "3️⃣ Attendance & Eligibility\n"
    "4️⃣ Scholarship Status\n"
    "5️⃣ Certificate Status\n"
    "6️⃣ Renewal Status\n"
    "7️⃣ Talk to Support\n\n"
    "Reply with the option number (1-7)."
)


def get_registration_status(ullas_id: str) -> str:
    """1️⃣ Registration Status"""
    reg = REGISTRATION.get(ullas_id)
    if reg is None:
        return "⚠️ No registration record found for your account."

    if reg["status"] == "VERIFIED":
        return (
            f"✅ *Registration Status:* VERIFIED\n"
            f"📅 Verified on: {reg['verified_on']}\n"
            f"🆔 Ullas ID: {ullas_id}\n\n"
            f"You are eligible for {reg['eligible_for']}."
        )
    else:
        return (
            f"❌ *Registration Status:* {reg['status']}\n"
            f"📝 Reason: {reg.get('reason', 'N/A')}\n"
            f"👉 {reg.get('action', 'Please contact support.')}"
        )


def get_exam_centre(ullas_id: str) -> str:
    """2️⃣ Exam Centre Details"""
    centre = EXAM_CENTRES.get(ullas_id)
    if centre is None:
        return "⚠️ No exam centre information found for your account."

    if centre.get("allocated"):
        return (
            f"🏫 *Exam Centre:* {centre['centre_name']}\n"
            f"📍 Location: {centre['location']}\n"
            f"🕘 Reporting Time: {centre['reporting_time']}\n"
            f"🗓 Exam Date: {centre['exam_date']}"
        )
    else:
        return (
            "⚠️ *Centre Not Yet Allocated*\n"
            "Please check again after the allocation date."
        )


def get_attendance(ullas_id: str) -> str:
    """3️⃣ Attendance & Eligibility"""
    att = ATTENDANCE.get(ullas_id)
    if att is None:
        return "⚠️ No attendance records found for your account."

    status_emoji = "🎯" if att["eligible"] else "⚠️"
    return (
        f"📊 *Attendance Summary:*\n\n"
        f"Summit 1: {att['summit_1']}\n"
        f"Summit 2: {att['summit_2']}\n"
        f"Summit 3: {att['summit_3']}\n"
        f"Summit 4: {att['summit_4']}\n\n"
        f"📈 Total Attendance: {att['total_percentage']}%\n\n"
        f"{status_emoji} *Eligibility Status:* {att['eligibility_note']}"
    )


def get_scholarship_status(ullas_id: str) -> str:
    """4️⃣ Scholarship Status"""
    sch = SCHOLARSHIP.get(ullas_id)
    if sch is None:
        return "⚠️ No scholarship record found for your account."

    lines = []
    # First scholarship
    first = sch.get("first", {})
    if first.get("status") == "Processed":
        lines.append(
            f"💰 *1st Scholarship ({first['amount']}):* Processed\n"
            f"📅 Date: {first['date']}\n"
            f"🏦 Bank: {first['bank']}\n"
            f"✅ Status: {first['transfer_status']}"
        )
    elif first.get("status") == "Failed":
        lines.append(
            f"❌ *1st Scholarship:* Payment Failed\n"
            f"📝 Reason: {first.get('reason', 'N/A')}\n"
            f"👉 {first.get('action', 'Contact support.')}"
        )
    else:
        lines.append(f"⏳ *1st Scholarship:* {first.get('status', 'N/A')}")

    lines.append("")  # blank line

    # Second scholarship
    second = sch.get("second", {})
    if second.get("status") == "Processed":
        lines.append(
            f"💰 *2nd Scholarship ({second['amount']}):* Processed\n"
            f"📅 Date: {second['date']}\n"
            f"🏦 Bank: {second['bank']}\n"
            f"✅ Status: {second['transfer_status']}"
        )
    elif second.get("status") == "Pending":
        lines.append(
            f"⏳ *2nd Scholarship:* Pending\n"
            f"📝 Reason: {second.get('reason', 'N/A')}"
        )
    else:
        lines.append(f"⏳ *2nd Scholarship:* {second.get('status', 'N/A')}")

    return "\n".join(lines)


def get_certificate_status(ullas_id: str) -> str:
    """5️⃣ Certificate Status"""
    cert = CERTIFICATES.get(ullas_id)
    if cert is None:
        return "⚠️ No certificate record found for your account."

    if cert.get("available"):
        return (
            f"🎓 *{cert['type']}:* Available\n"
            f"📅 Event: {cert['event']}\n"
            f"🔗 Download Link: {cert['download_link']}"
        )
    else:
        return (
            f"❌ *Certificate Not Available*\n"
            f"📝 Reason: {cert.get('reason', 'N/A')}"
        )


def get_renewal_status(ullas_id: str) -> str:
    """6️⃣ Renewal Status"""
    ren = RENEWAL.get(ullas_id)
    if ren is None:
        return (
            "⚠️ *No Renewal Record Found*\n"
            "Please contact your school SPOC."
        )

    return (
        f"🔄 *Student Category:* {ren['category']}\n"
        f"📚 Class: {ren['current_class']}\n"
        f"🎓 Batch Year: {ren['batch_year']}"
    )


def talk_to_support() -> str:
    """7️⃣ Talk to Support"""
    return (
        "📞 *Ullas Support*\n\n"
        "You can reach our support team via:\n"
        "📧 Email: support@ullas.example.com\n"
        "📱 Helpline: 1800-XXX-XXXX (Toll-free)\n"
        "🕘 Available: Mon–Sat, 9 AM – 6 PM\n\n"
        "An agent will get back to you shortly."
    )


# Map menu option number → handler
MENU_HANDLERS = {
    "1": ("Registration Status", get_registration_status),
    "2": ("Exam Centre Details", get_exam_centre),
    "3": ("Attendance & Eligibility", get_attendance),
    "4": ("Scholarship Status", get_scholarship_status),
    "5": ("Certificate Status", get_certificate_status),
    "6": ("Renewal Status", get_renewal_status),
}
>>>>>>> dcac34ae394b737d3d1a4418eaed2730891f06a7
