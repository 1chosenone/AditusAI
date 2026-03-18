from fastapi import APIRouter
from core.queue import get_job_status
from schemas.responses import JobStatusResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobStatusResponse, tags=["jobs"])
def fetch_job_status(job_id: str):
    return get_job_status(job_id)
