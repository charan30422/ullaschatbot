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
sessions: dict = {}


def _now() -> float:
    """Current epoch time."""
    return time.time()


def get_session(phone: str) -> Optional[dict]:
    """Return the active session for phone, or None if missing / expired."""
    sess = sessions.get(phone)
    if sess is None:
        logger.debug("get_session(%s) → no session found", phone)
        return None
    age = _now() - sess.get("last_activity", 0)
    if age > SESSION_TIMEOUT_SECONDS:
        logger.info("get_session(%s) → session expired after %.0fs (limit=%ss)", phone, age, SESSION_TIMEOUT_SECONDS)
        sessions.pop(phone, None)
        return None
    logger.debug("get_session(%s) → active session state=%s age=%.0fs", phone, sess.get("state"), age)
    return sess


def start_session(phone: str) -> dict:
    """Create and return a fresh session for the given phone number."""
    sessions[phone] = {
        "ullas_id":      None,
        "state":         "awaiting_id",
        "last_activity": _now(),
    }
    logger.info("start_session(%s) → new session created, total active sessions: %d", phone, len(sessions))
    return sessions[phone]


def lookup_student(identifier: str) -> Optional[str]:
    """
    Look up a student by Ullas ID or registered phone number.
    Returns the matching ullas_id or None.
    """
    logger.debug("lookup_student: checking identifier [%s]", identifier)

    # Direct Ullas ID match
    if identifier in STUDENTS:
        logger.debug("lookup_student: direct STUDENTS match → %s", identifier)
        return identifier

    # Phone number match — normalise
    clean = identifier.lstrip("+").replace(" ", "").replace("-", "")
    logger.debug("lookup_student: normalised phone = [%s], checking PHONE_TO_ULLAS", clean)
    logger.debug("lookup_student: known phones = %s", list(PHONE_TO_ULLAS.keys()))

    result = PHONE_TO_ULLAS.get(clean)
    if result:
        logger.debug("lookup_student: phone match found → %s", result)
    else:
        logger.warning("lookup_student: no match for [%s] (raw) / [%s] (clean)", identifier, clean)
    return result


def touch_session(phone: str) -> None:
    """Refresh the last_activity timestamp so the session doesn't expire."""
    sess = sessions.get(phone)
    if sess:
        sess["last_activity"] = _now()
        logger.debug("touch_session(%s) → last_activity refreshed", phone)


def clear_session(phone: str) -> None:
    """Delete the session for the given phone number."""
    existed = phone in sessions
    sessions.pop(phone, None)
    logger.info("clear_session(%s) → removed=%s, remaining sessions: %d", phone, existed, len(sessions))
