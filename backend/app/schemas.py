"""
NoteGuard AI - Pydantic v2 Request & Response Schemas
=====================================================
Strict validation schemas for API contracts.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ImageQualitySchema(BaseModel):
    is_acceptable: bool = True
    status: str = Field(..., description="Good | Acceptable | Poor")
    blur_score: float = Field(..., description="Laplacian variance sharpness")
    brightness: float = Field(..., description="Normalized brightness in [0.0, 1.0]")
    glare_ratio: float = Field(..., description="Percentage of glare reflection")
    message: Optional[str] = None
    warnings: List[str] = []


class PredictionResponse(BaseModel):
    success: bool = True
    status: str = Field(default="success", description="success | warning | error")
    id: Optional[int] = None
    denomination: Any = Field(..., description="e.g. 500 or '₹500' or 'Unknown'")
    currency: str = Field(default="INR", description="ISO currency code")
    currency_symbol: str = Field(default="₹", description="Currency symbol")
    denomination_label: str = Field(..., description="Display label e.g. '₹500' or 'Unknown Denomination'")
    circulation_status: str = Field(default="Circulating Legal Tender", description="Circulating Legal Tender | Withdrawn from Circulation | Historical / Demone­tized | Unknown")
    authenticity: str = Field(..., description="Likely Genuine | Suspected Fake | Uncertain / Unable to Verify")
    denomination_confidence: float = Field(default=0.0, description="Stage 1 Denomination model confidence [0.0, 1.0]")
    authenticity_confidence: float = Field(default=0.0, description="Stage 2 Authenticity model confidence [0.0, 1.0]")
    predicted_class: str = Field(default="genuine", description="genuine | fake | uncertain")
    genuine_score: float = Field(default=0.0, description="Model probability for genuine class [0.0, 1.0]")
    fake_score: float = Field(default=0.0, description="Model probability for counterfeit class [0.0, 1.0]")
    confidence: float = Field(..., description="Primary classification confidence [0.0, 1.0]")
    decision_status: str = Field(default="likely_genuine", description="likely_genuine | suspected_fake | uncertain | invalid_image")
    status_label: str = Field(..., description="Verification classification category")
    warning: str = Field(default="This AI result is a preliminary screening estimate, not official currency authentication. Camera images cannot verify every physical security feature. If authenticity is uncertain, inspect the note's security features and consult an appropriate bank.")
    disclaimer: str = Field(default="This AI result is a preliminary screening estimate, not official currency authentication. Camera images cannot verify every physical security feature. If authenticity is uncertain, inspect the note's security features and consult an appropriate bank.")
    model_version: str = Field(default="EfficientNetB0-v2.1", description="Active model architecture version")
    security_features: Optional[Dict[str, Any]] = None
    image_quality: ImageQualitySchema
    original_image_url: str
    gradcam_url: Optional[str] = None
    inference_time_ms: Optional[float] = None


class CameraPredictionRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded JPEG/PNG image data from webcam")


class HistoryItemResponse(BaseModel):
    id: int
    timestamp: Optional[str]
    filename: str
    original_image_url: str
    gradcam_url: Optional[str]
    denomination: str
    authenticity: str
    confidence: float
    status_label: str
    warning: Optional[str]
    image_quality: Dict[str, Any]


class HistoryListResponse(BaseModel):
    total: int
    records: List[HistoryItemResponse]
