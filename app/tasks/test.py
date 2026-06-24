from ..db.database import SessionLocal
from ..db import models
from ..service import ai_service
from upstash_redis import Redis
from ..core.config import settings
import hashlib
import json

redis_client = Redis(
    url=settings.UPSTASH_REDIS_REST_URL,
    token=settings.UPSTASH_REDIS_REST_TOKEN
)

def generate_idea_analysis(idea: str, user_id: int):
    db = SessionLocal()
    print("🔥 WORKER STARTED")
    print("IDEA:", idea)
    print("USER_ID:", user_id)

    try:
        cache_key = hashlib.sha256(idea.encode()).hexdigest()

        cached = redis_client.get(cache_key)

        if cached:
            final_analysis = json.loads(cached)
        else:
            prompt1 = ai_service.get_prompt1(idea)

            if prompt1.get("error"):
                return {"error": prompt1["error"]}

            whole_analysis = ai_service.get_analysis(
                idea=idea,
                core_features=prompt1["core_features"],
                db_design=prompt1["db_design"]
            )

            final_analysis = {**prompt1, **whole_analysis}

            redis_client.set(cache_key, json.dumps(final_analysis), ex=3600)

        new_analysis = models.blueprints(
            developer_idea=idea,
            user_id=user_id,
            app_type=final_analysis["app_type"],
            core_features=final_analysis["core_features"],
            target_users=final_analysis["target_users"],
            db_design=final_analysis["db_design"],
            end_points=final_analysis["end_points"],
            risk_factors=final_analysis["risk_areas"],
            roadmap=final_analysis["roadmap"]
        )

        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        
        print("✅ AFTER COMMIT DONE")
        print("NEW ID:", new_analysis.id)

        return {
            "analysis": final_analysis,
            "id": new_analysis.id
        }

    finally:
        db.close()