from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import session
from ..db.database import get_db
from ..db import models
from ..core.security import get_current_user 
from ..schemas import ventures
from ..service import ai_service

router = APIRouter()

@router.post("/idea_analysis")
def get_analysis(venture:ventures.UserIdea, db:session=Depends(get_db), current_user = Depends(get_current_user)):
    try:
        prompt1 = ai_service.get_prompt1(venture.idea)
        error = prompt1.get("error")   
        if error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)     
        whole_analysis = ai_service.get_analysis(idea= venture.idea, core_features=prompt1["core_features"], db_design=prompt1["db_design"])
        final_analysis = {**prompt1, **whole_analysis}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    new_analysis = models.blueprints(
                    developer_idea = venture.idea,
                    user_id = current_user.id,
                    app_type = final_analysis["app_type"],
                    core_features = final_analysis["core_features"],
                    target_users = final_analysis["target_users"],
                    db_design = final_analysis["db_design"],
                    end_points = final_analysis["end_points"],
                    risk_factors = final_analysis["risk_areas"],
                    roadmap = final_analysis["roadmap"]
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return final_analysis