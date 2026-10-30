"""
NoteGuard AI - Live Camera Route Handlers
=========================================
Receives live webcam/camera frames captured via browser WebRTC/MediaDevices.
Supports both base64 JSON payload and multipart binary frame uploads.
"""

import base64
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PredictionResponse, CameraPredictionRequest
from app.utils.helpers import generate_unique_filename
from app.services.prediction_service import run_prediction_pipeline

router = APIRouter(prefix="/api", tags=["Camera"])


@router.post("/predict/camera", response_model=PredictionResponse)
async def predict_camera_frame(
    payload: CameraPredictionRequest = Body(...),
    db: Session = Depends(get_db)
):
    """
    Screens an Indian banknote frame captured from the device camera.
    Decodes Base64 data URL, checks quality, runs models, and computes Grad-CAM.
    """
    raw_b64 = payload.image_base64
    # Strip base64 metadata header if present (e.g. 'data:image/jpeg;base64,')
    if "," in raw_b64:
        raw_b64 = raw_b64.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(raw_b64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 encoding: {str(e)}")

    if len(image_bytes) < 100:
        raise HTTPException(status_code=400, detail="Captured camera image is empty or invalid.")

    filename = generate_unique_filename(".jpg")
    try:
        result = run_prediction_pipeline(
            image_bytes=image_bytes,
            original_filename=f"camera_{filename}",
            db=db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Camera screening inference failed: {str(e)}")
