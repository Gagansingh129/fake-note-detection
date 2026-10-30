"""
NoteGuard AI - Prediction Route Handlers
========================================
Endpoints for uploading banknote images and receiving screening assessments.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PredictionResponse
from app.utils.helpers import validate_image_file, generate_unique_filename
from app.services.prediction_service import run_prediction_pipeline

router = APIRouter(prefix="/api", tags=["Prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_note(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Screens an uploaded currency note image:
    - Validates file type and size.
    - Evaluates image sharpness and lighting.
    - Infers denomination (₹100 - ₹500).
    - Predicts authenticity (Genuine vs Potentially Fake).
    - Generates Explainable AI Grad-CAM heatmap.
    - Saves record in audit history.
    """
    content = await file.read()
    validate_image_file(file, content)

    safe_name = generate_unique_filename(file.filename or "uploaded.jpg")
    try:
        result = run_prediction_pipeline(
            image_bytes=content,
            original_filename=safe_name,
            db=db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failure: {str(e)}")
