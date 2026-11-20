"""
NoteGuard AI - Authentication REST API Endpoints
================================================
Provides user registration, login, demo access, session verification, and logout.
"""

from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_session_token,
    get_user_from_token,
    ensure_demo_user,
    SESSION_TOKENS
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Registers a new user account."""
    username = req.username.strip().lower()
    email = req.email.strip().lower()

    if len(req.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long."
        )

    # Check for existing user
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{username}' is already taken."
        )
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{email}' is already registered."
        )

    new_user = User(
        username=username,
        email=email,
        full_name=req.full_name or username,
        password_hash=hash_password(req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_session_token(new_user)
    return {
        "success": True,
        "message": "Account created successfully.",
        "token": token,
        "user": new_user.to_dict()
    }


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticates user with username or email and password."""
    identifier = req.username_or_email.strip().lower()
    user = db.query(User).filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )

    token = create_session_token(user)
    return {
        "success": True,
        "message": "Login successful.",
        "token": token,
        "user": user.to_dict()
    }


@router.post("/demo")
def demo_login(db: Session = Depends(get_db)):
    """Provides one-click instant login as lead analyst for frictionless demonstration."""
    user = ensure_demo_user(db)
    token = create_session_token(user)
    return {
        "success": True,
        "message": "Logged in as Lead Currency Analyst.",
        "token": token,
        "user": user.to_dict()
    }


@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Returns currently authenticated user profile."""
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    token = authorization.replace("Bearer ", "").strip()
    user = get_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid.")

    return {
        "success": True,
        "user": user.to_dict()
    }


@router.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    """Logs out and invalidates the session token."""
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        SESSION_TOKENS.pop(token, None)
    return {"success": True, "message": "Logged out successfully."}

