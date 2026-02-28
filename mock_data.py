"""
Mock data for the Ullas WhatsApp Chatbot.
Simulates Oracle DB responses for all query categories.
Replace this module with real DB queries when Oracle is connected.
"""

# ---------- Mock Student Database ----------
# Keyed by Ullas ID; phone numbers map to Ullas IDs via PHONE_TO_ULLAS
STUDENTS = {
    "UL-09-2026-00456": {
        "name": "Rahul Sharma",
        "phone": "919876543210",
        "class": "9",
        "batch_year": "2026",
    },
    "UL-10-2025-00789": {
        "name": "Priya Patel",
        "phone": "919876543211",
        "class": "10",
        "batch_year": "2025",
    },
    "UL-11-2024-01023": {
        "name": "Amit Kumar",
        "phone": "919876543212",
        "class": "11",
        "batch_year": "2024",
    },
}

# Reverse lookup: phone → ullas_id
PHONE_TO_ULLAS = {s["phone"]: uid for uid, s in STUDENTS.items()}

# ---------- 1. Registration Status ----------
REGISTRATION = {
    "UL-09-2026-00456": {
        "status": "VERIFIED",
        "verified_on": "12 July 2026",
        "eligible_for": "CAN-DO Workshop",
    },
    "UL-10-2025-00789": {
        "status": "REJECTED",
        "reason": "Bank Passbook not clear",
        "action": "Please re-upload via app",
    },
    "UL-11-2024-01023": {
        "status": "VERIFIED",
        "verified_on": "05 March 2024",
        "eligible_for": "CAN-DO Workshop",
    },
}

# ---------- 2. Exam Centre Details ----------
EXAM_CENTRES = {
    "UL-09-2026-00456": {
        "allocated": True,
        "centre_name": "St. Mary's High School",
        "location": "Andheri East, Mumbai",
        "reporting_time": "8:30 AM",
        "exam_date": "12 March 2026",
    },
    "UL-10-2025-00789": {
        "allocated": False,
    },
    "UL-11-2024-01023": {
        "allocated": True,
        "centre_name": "Delhi Public School",
        "location": "Dwarka, New Delhi",
        "reporting_time": "9:00 AM",
        "exam_date": "15 March 2024",
    },
}

# ---------- 3. Attendance ----------
ATTENDANCE = {
    "UL-09-2026-00456": {
        "summit_1": "Present",
        "summit_2": "Present",
        "summit_3": "Absent",
        "summit_4": "Present",
        "total_percentage": 75,
        "eligible": True,
        "eligibility_note": "Eligible for 2nd Scholarship",
    },
    "UL-10-2025-00789": {
        "summit_1": "Present",
        "summit_2": "Absent",
        "summit_3": "Absent",
        "summit_4": "Absent",
        "total_percentage": 25,
        "eligible": False,
        "eligibility_note": "NOT eligible for 2nd NEFT. Minimum Required: 60%",
    },
    "UL-11-2024-01023": {
        "summit_1": "Present",
        "summit_2": "Present",
        "summit_3": "Present",
        "summit_4": "Present",
        "total_percentage": 100,
        "eligible": True,
        "eligibility_note": "Eligible for 2nd Scholarship",
    },
}

# ---------- 4. Scholarship Status ----------
SCHOLARSHIP = {
    "UL-09-2026-00456": {
        "first": {
            "status": "Processed",
            "amount": "50%",
            "date": "14 August 2026",
            "bank": "SBI",
            "transfer_status": "Successful",
        },
        "second": {
            "status": "Pending",
            "reason": "Awaiting attendance validation",
        },
    },
    "UL-10-2025-00789": {
        "first": {
            "status": "Failed",
            "reason": "Invalid IFSC Code",
            "action": "Please update bank details in the app",
        },
        "second": {
            "status": "Pending",
            "reason": "First scholarship not cleared",
        },
    },
    "UL-11-2024-01023": {
        "first": {
            "status": "Processed",
            "amount": "50%",
            "date": "10 June 2024",
            "bank": "HDFC",
            "transfer_status": "Successful",
        },
        "second": {
            "status": "Processed",
            "amount": "50%",
            "date": "20 December 2024",
            "bank": "HDFC",
            "transfer_status": "Successful",
        },
    },
}

# ---------- 5. Certificate Status ----------
CERTIFICATES = {
    "UL-09-2026-00456": {
        "available": True,
        "type": "Participation Certificate",
        "event": "Summit 2026",
        "download_link": "https://ullas.example.com/cert/UL-09-2026-00456",
    },
    "UL-10-2025-00789": {
        "available": False,
        "reason": "Attendance below required threshold",
    },
    "UL-11-2024-01023": {
        "available": True,
        "type": "Participation Certificate",
        "event": "Summit 2024",
        "download_link": "https://ullas.example.com/cert/UL-11-2024-01023",
    },
}

# ---------- 6. Renewal Status ----------
RENEWAL = {
    "UL-09-2026-00456": None,  # New student — no renewal record
    "UL-10-2025-00789": {
        "category": "Renewal",
        "current_class": "10",
        "batch_year": "2025",
    },
    "UL-11-2024-01023": {
        "category": "Renewal",
        "current_class": "11",
        "batch_year": "2024",
    },
}
