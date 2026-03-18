"""Redis Queue (RQ) job queue management."""

from typing import Any, Callable, Optional
from core.config import settings
from redis import Redis
from rq import Queue
from rq.job import Job

redis_conn = Redis.from_url(settings.redis_url)
q = Queue("default", connection=redis_conn)


def enqueue(func: Callable, *args: Any, job_timeout="5m", **kwargs: Any) -> str:
    """Enqueue a function to run as a background job.

    Args:
        func: The function to execute.
        *args: Positional arguments passed to the function.
        job_timeout: Maximum time the job can run before being terminated.
        **kwargs: Keyword arguments passed to the function.

    Returns:
        The unique job ID.
    """
    job = q.enqueue(func, *args, job_timeout=job_timeout, **kwargs)
    return job.id


def get_job(job_id: str) -> Optional[Job]:
    """Fetch a job by its ID.

    Args:
        job_id: The unique identifier of the job.

    Returns:
        The Job object if found, None otherwise.
    """
    try:
        return Job.fetch(job_id, connection=redis_conn)
    except Exception:
        return None


def get_job_status(job_id: str) -> dict[str, Any]:
    """Get the status of a background job.

    Args:
        job_id: The unique identifier of the job.

    Returns:
        dict with id, status, result, and error fields.
    """
    job = get_job(job_id)

    if not job:
        return {"status": "not_found"}

    return {
        "id": job.id,
        "status": job.get_status(),
        "result": job.result,
        "error": job.exc_info if job.is_failed else None,
    }
