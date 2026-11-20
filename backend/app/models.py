"""
NoteGuard AI - SQLAlchemy Database Models
=========================================
Defines the schema for storing screening audit records and metadata.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from app.database import Base


class User(Base):
    """User account entity for login and authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name or self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class PredictionRecord(Base):
    """Stores inference metadata, predictions, quality diagnostics, and image references."""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Image Identifiers
    filename = Column(String(255), nullable=False)
    original_image_url = Column(String(255), nullable=False)
    gradcam_url = Column(String(255), nullable=True)

    # Predictions
    denomination = Column(String(50), nullable=False, default="Unknown")
    authenticity = Column(String(50), nullable=False)  # "Genuine" | "Potentially Fake"
    confidence = Column(Float, nullable=False)         # 0.0 to 1.0
    status_label = Column(String(50), nullable=False)  # "Verified Genuine", "Potentially Counterfeit", "Uncertain"
    warning = Column(Text, nullable=True)

    # Quality Diagnostics
    quality_status = Column(String(50), nullable=False, default="Good")  # "Good" | "Acceptable" | "Poor"
    blur_score = Column(Float, nullable=True)
    brightness = Column(Float, nullable=True)
    glare_ratio = Column(Float, nullable=True)

    def to_dict(self):
        """Converts model entity to dictionary for API responses."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "filename": self.filename,
            "original_image_url": self.original_image_url,
            "gradcam_url": self.gradcam_url,
            "denomination": self.denomination,
            "authenticity": self.authenticity,
            "confidence": round(self.confidence, 4),
            "status_label": self.status_label,
            "warning": self.warning,
            "image_quality": {
                "status": self.quality_status,
                "blur_score": self.blur_score,
                "brightness": self.brightness,
                "glare_ratio": self.glare_ratio
            }
        }
