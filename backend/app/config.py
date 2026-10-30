"""
NoteGuard AI - Application Configuration & Thresholds
=====================================================
Centralized settings for backend services, model paths, security limits,
CORS policies, and screening confidence thresholds.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "NoteGuard AI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # Directory Paths
    STATIC_UPLOADS_DIR: Path = BASE_DIR / "uploads"
    STATIC_RESULTS_DIR: Path = PROJECT_ROOT / "results"
    MODELS_DIR: Path = BASE_DIR / "models"
    
    # Model Artifact Paths
    DENOMINATION_MODEL_PATH: Path = MODELS_DIR / "denomination_model.keras"
    AUTHENTICITY_MODEL_PATH: Path = MODELS_DIR / "authenticity_model.keras"
    BASELINE_MODEL_PATH: Path = MODELS_DIR / "baseline_cnn.keras"
    CLASS_NAMES_PATH: Path = MODELS_DIR / "class_names.json"

    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'app' / 'noteguard.db'}"

    # File Security Limits
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB maximum
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".webp"}
    ALLOWED_MIME_TYPES: set = {"image/jpeg", "image/png", "image/webp"}

    # Screening Confidence Thresholds
    CONFIDENCE_HIGH: float = 0.80      # >= 0.80: Display prediction with high confidence
    CONFIDENCE_UNCERTAIN: float = 0.60 # 0.60 - 0.79: Flag as Uncertain recapture recommendation
                                       # < 0.60: Low confidence / High uncertainty

    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure critical directories exist
settings.STATIC_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
(settings.STATIC_RESULTS_DIR / "gradcam").mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
