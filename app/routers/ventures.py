from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import session
from ..db.database import get_db
from ..db import models
from ..core.security import get_current_user 
from ..schemas import ventures
from ..service import ai_service
from upstash_redis import Redis
from ..core.config import settings
import hashlib
import json

redis_client = Redis(
    url=settings.UPSTASH_REDIS_REST_URL,
    token=settings.UPSTASH_REDIS_REST_TOKEN
)

router = APIRouter()

@router.post("/idea_analysis")
def get_analysis(venture:ventures.UserIdea, db:session=Depends(get_db), current_user = Depends(get_current_user)):
    cache_key = hashlib.sha256(
            venture.idea.encode()
        ).hexdigest()

    cached = redis_client.get(cache_key)

    if cached:
        final_analysis = json.loads(cached)

    else :
        try:
            prompt1 = ai_service.get_prompt1(venture.idea)
            error = prompt1.get("error")   
            if error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)     
            whole_analysis = ai_service.get_analysis(idea= venture.idea, core_features=prompt1["core_features"], db_design=prompt1["db_design"])
            final_analysis = {**prompt1, **whole_analysis}
            redis_client.set(
                    cache_key,
                    json.dumps(final_analysis),
                    ex=3600
            )

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
    return{**final_analysis, "id": new_analysis.id}