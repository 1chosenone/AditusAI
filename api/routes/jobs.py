"""Job status API routes."""

from fastapi import APIRouter
from core.queue import get_job_status
from schemas.responses import JobStatusResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobStatusResponse)
def fetch_job_status(job_id: str):
    """Retrieve the status of a background job.

    Args:
        job_id: The unique identifier of the job.

    Returns:
        JobStatusResponse with job status, result, and error if any.
    """
    return get_job_status(job_id)
