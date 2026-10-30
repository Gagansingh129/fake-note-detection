"""
NoteGuard AI - Audit History Route Handlers
===========================================
Queries and manages stored currency screening audit records.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import PredictionRecord
from app.schemas import HistoryListResponse, HistoryItemResponse

router = APIRouter(prefix="/api", tags=["History"])


@router.get("/history", response_model=HistoryListResponse)
def get_prediction_history(
    filter_by: Optional[str] = Query(None, description="all | genuine | fake | uncertain"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Retrieves chronological list of past currency note screening predictions."""
    query = db.query(PredictionRecord)

    if filter_by:
        f = filter_by.lower()
        if f == "genuine":
            query = query.filter(PredictionRecord.authenticity.ilike("%genuine%"))
        elif f in ["fake", "potentially fake", "churan", "suspected fake"]:
            query = query.filter(PredictionRecord.authenticity.ilike("%fake%"))
        elif f in ["uncertain", "inconclusive"]:
            query = query.filter(
                (PredictionRecord.authenticity.ilike("%uncertain%")) |
                (PredictionRecord.status_label.ilike("%uncertain%"))
            )

    total = query.count()
    records = query.order_by(desc(PredictionRecord.timestamp)).limit(limit).all()

    return {
        "total": total,
        "records": [r.to_dict() for r in records]
    }


@router.get("/history/{record_id}", response_model=HistoryItemResponse)
def get_history_detail(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Retrieves specific screening record by primary key."""
    record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Screening record #{record_id} not found.")
    return record.to_dict()


@router.delete("/history/{record_id}")
def delete_history_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Deletes an audit history entry from SQLite."""
    record = db.query(PredictionRecord).filter(PredictionRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Record #{record_id} not found.")
    
    db.delete(record)
    db.commit()
    return {"success": True, "message": f"Record #{record_id} deleted successfully."}
