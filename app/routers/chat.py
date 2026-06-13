from sqlalchemy.orm import session
from fastapi import HTTPException, status, APIRouter, Depends
from ..db import models
from ..schemas.chat import ChatQuestion
from ..db.database import get_db
from ..core.security import get_current_user
from ..service import chat_service

router = APIRouter()

def fetch_conversations(id:int, db:session):
    conversations = db.query(models.blueprints).filter(models.blueprints.id==id).first()

    if not conversations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    
    return{
            "analysis_id" : conversations.id,
            "user_id" : conversations.user_id,
            "developer_idea" : conversations.developer_idea,
            "app_type" : conversations.app_type,
            "core_features" : conversations.core_features,
            "target_users" : conversations.target_users,
            "db_design" : conversations.db_design,
            "end_points" : conversations.end_points,
            "roadmap" : conversations.roadmap,
            "risk_factors" : conversations.risk_factors
    }


@router.post("/analysis/{id}/")
def store_messages(question:ChatQuestion, id:int, db:session=Depends(get_db), current_user = Depends(get_current_user)):
    try:
        analysis = fetch_conversations(id,db) 

        if analysis["user_id"] != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "INVALID CREDENTIALS")
        
        chat_response = chat_service.chat_prompt(question=question.question, idea = analysis["developer_idea"], analysis=analysis)

        error = chat_response.get("error",None)
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
        new_message = models.Messages(
                    analysis_id = id,
                    question = question.question,
                    answer = chat_response["answer"]
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "AI SERVICE FAILED. PLEASE TRY AGAIN")
    return chat_response
