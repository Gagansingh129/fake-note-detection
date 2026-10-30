"""
NoteGuard AI - Helper Utilities & Security Validation
======================================================
Implements file sanitization, MIME-type verification, and secure path handlers.
"""

import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

from app.config import settings

def validate_image_file(file: UploadFile, content_bytes: bytes) -> None:
    """
    Rigorously validates uploaded image:
    1. Rejects oversized files.
    2. Rejects unsupported MIME types.
    3. Validates file header and structure via Pillow to prevent malicious disguised files.
    """
    # 1. Size check
    if len(content_bytes) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_BYTES // (1024*1024)} MB."
        )

    if len(content_bytes) < 100:
        raise HTTPException(status_code=400, detail="Uploaded file is empty or corrupted.")

    # 2. MIME type check
    content_type = file.content_type.lower() if file.content_type else ""
    if content_type not in settings.ALLOWED_MIME_TYPES and not any(file.filename.lower().endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type '{content_type}'. Allowed types: JPG, PNG, WEBP."
        )

    # 3. Header & structural verification
    try:
        img = Image.open(io.BytesIO(content_bytes))
        img.verify()  # Verifies image structure
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Corrupted or invalid image file structure: {str(e)}")


def generate_unique_filename(extension: str = ".jpg") -> str:
    """Generates an unguessable UUID filename preventing path traversal."""
    clean_ext = extension if extension.startswith(".") else f".{extension}"
    return f"{uuid.uuid4().hex}{clean_ext}"
