from fastapi import APIRouter, Depends
from ..core.security import get_current_user 
from ..schemas import ventures
from ..tasks.test import generate_idea_analysis
from rq import Queue
from redis import Redis
from rq.job import Job
from ..core.config import settings


router = APIRouter()

redis_conn = Redis.from_url(settings.REDIS_URL)
queue = Queue(connection=redis_conn)

@router.post("/idea_analysis")
def get_analysis(
    venture: ventures.UserIdea,
    current_user=Depends(get_current_user)
):
    

    job = queue.enqueue(
        generate_idea_analysis,
        venture.idea,
        current_user.id
    )

    return {
        "job_id": job.id,
        "status": "processing"
    }


@router.get("/jobs/{job_id}")
def get_job(job_id: str):

    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return {
            "status": "completed",
            "result": job.result
        }

    if job.is_failed:
        return {
            "status": "failed",
            "error": str(job.exc_info)
        }

    return {
        "status": "processing"
    } 
