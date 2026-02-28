"""
Session management for the Ullas chatbot.
All state is held in-memory (suitable for single-process deployment).
"""
import time
import logging
from typing import Optional

from config import SESSION_TIMEOUT_SECONDS
from mock_data import PHONE_TO_ULLAS, STUDENTS

logger = logging.getLogger(__name__)

# ----- In-memory session store -----
# sessions[phone] = {
#     "ullas_id": str | None,
#     "state":    "awaiting_id" | "menu",
#     "last_activity": float,
# }
sessions: dict = {}


def _now() -> float:
    """Current epoch time."""
    return time.time()


def get_session(phone: str) -> Optional[dict]:
    """Return the active session for phone, or None if missing / expired."""
    sess = sessions.get(phone)
    if sess is None:
        return None
    if _now() - sess.get("last_activity", 0) > SESSION_TIMEOUT_SECONDS:
        logger.info("Session timed out for %s", phone)
        sessions.pop(phone, None)
        return None
    return sess


def start_session(phone: str) -> dict:
    """Create and return a fresh session for the given phone number."""
    sessions[phone] = {
        "ullas_id":     None,
        "state":        "awaiting_id",
        "last_activity": _now(),
    }
    return sessions[phone]


def lookup_student(identifier: str) -> Optional[str]:
    """
    Look up a student by Ullas ID or registered phone number.

    Args:
        identifier: Ullas ID (e.g. "UL-09-2026-00456") or phone number
                    in any common format (e.g. "+919876543210" or "919876543210")

    Returns:
        The matching ullas_id string, or None if not found.
    """
    # Direct Ullas ID match
    if identifier in STUDENTS:
        return identifier

    # Phone number match — normalise by stripping +, spaces, dashes
    clean = identifier.lstrip("+").replace(" ", "").replace("-", "")
    return PHONE_TO_ULLAS.get(clean)  # returns None if not found


def touch_session(phone: str) -> None:
    """Refresh the last_activity timestamp so the session doesn't expire."""
    sess = sessions.get(phone)
    if sess:
        sess["last_activity"] = _now()


def clear_session(phone: str) -> None:
    """Delete the session for the given phone number."""
    sessions.pop(phone, None)
