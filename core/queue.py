from typing import Any, Callable, Optional
from core.config import settings
from redis import Redis
from rq import Queue
from rq.job import Job

redis_conn = Redis.from_url(settings.redis_url)
q = Queue("default", connection=redis_conn)


def enqueue(func: Callable, *args: Any, job_timeout="5m", **kwargs: Any) -> str:
    job = q.enqueue(func, *args, job_timeout=job_timeout, **kwargs)
    return job.id


def get_job(job_id: str) -> Optional[Job]:
    try:
        return Job.fetch(job_id, connection=redis_conn)
    except Exception:
        return None


def get_job_status(job_id: str):
    job = get_job(job_id)

    if not job:
        return {"status": "not_found"}

    return {
        "id": job.id,
        "status": job.get_status(),
        "result": job.result,
        "error": job.exc_info if job.is_failed else None,
    }
