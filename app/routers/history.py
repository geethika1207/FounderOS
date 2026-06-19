from fastapi import APIRouter, Depends, HTTPException, status
from ..db import models
from ..core.security import get_db
from sqlalchemy.orm import session
from ..core.security import get_current_user
from ..schemas.history import AnalysisResponse
from ..schemas.history import HistoryResponse
from typing import List
from sqlalchemy import func

router = APIRouter()

@router.get("/history/{id}", response_model=AnalysisResponse)
def get_analysis(id: int, db: session = Depends(get_db), current_user = Depends(get_current_user)):
    analysis = db.query(models.blueprints)\
        .outerjoin(models.Messages, models.blueprints.id == models.Messages.analysis_id)\
        .filter(
            models.blueprints.id == id,
            models.blueprints.user_id == current_user.id
        ).first()

    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    
    return analysis

@router.get("/history", response_model=List[HistoryResponse])
def get_history(limit: int = 3, db: session = Depends(get_db), current_user=Depends(get_current_user)):
    results = db.query(
        models.blueprints,
        func.count(models.Messages.id).label("message_count")).outerjoin(models.Messages, models.Messages.analysis_id == models.blueprints.id
        ).filter(models.blueprints.user_id == current_user.id).group_by(models.blueprints.id).limit(limit).all()

    output = [] 
    for analysis, message_count in results:
        output.append({
            "id": analysis.id,
            "developer_idea": analysis.developer_idea,
            "app_type": analysis.app_type,
            "created_at": analysis.created_at,
            "message_count": message_count
        })
    
    return output

@router.delete("/analysis/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(id: int, db: session = Depends(get_db), current_user=Depends(get_current_user)):
    analysis = db.query(models.blueprints).filter(models.blueprints.id == id, models.blueprints.user_id==current_user.id).first()

    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
     
    db.delete(analysis)
    db.commit()