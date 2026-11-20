"""
NoteGuard AI - Authentication & Password Security Service
=========================================================
Implements secure PBKDF2-HMAC-SHA256 password hashing, salt management,
and token generation for user authentication.
"""

import hashlib
import os
import secrets
import time
from typing import Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.models import User

# PBKDF2 Configuration
ITERATIONS = 120_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Generates a secure salted hash: salt$iterations$hash."""
    salt = secrets.token_hex(SALT_BYTES)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        ITERATIONS
    )
    return f"{salt}${ITERATIONS}${key.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verifies a plaintext password against the stored salted hash."""
    try:
        parts = stored_hash.split("$")
        if len(parts) != 3:
            return False
        salt, iterations_str, key_hex = parts
        iterations = int(iterations_str)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations
        )
        return secrets.compare_digest(key.hex(), key_hex)
    except Exception:
        return False


# In-memory session token store: token -> {user_id, expires_at}
SESSION_TOKENS: Dict[str, Dict[str, Any]] = {}
TOKEN_DURATION_SEC = 7 * 24 * 3600  # 7 days


def create_session_token(user: User) -> str:
    """Generates a secure session token and stores the session."""
    token = secrets.token_urlsafe(32)
    SESSION_TOKENS[token] = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name or user.username,
        "expires_at": time.time() + TOKEN_DURATION_SEC
    }
    return token


def get_user_from_token(token: str, db: Session) -> Optional[User]:
    """Retrieves the User object if token is valid and not expired."""
    session = SESSION_TOKENS.get(token)
    if not session:
        return None
    if time.time() > session["expires_at"]:
        SESSION_TOKENS.pop(token, None)
        return None
    return db.query(User).filter(User.id == session["user_id"]).first()


def ensure_demo_user(db: Session) -> User:
    """Ensures a default demo user exists for quick login in presentations."""
    user = db.query(User).filter((User.username == "analyst") | (User.email == "demo@noteguard.ai")).first()
    if not user:
        user = User(
            username="analyst",
            email="demo@noteguard.ai",
            full_name="Lead Currency Analyst",
            password_hash=hash_password("noteguard123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

