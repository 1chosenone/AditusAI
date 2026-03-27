import asyncio
from database.session import SESSION_LOCAL
from schemas.candidate import CandidateProfileSchema


def discover_jobs(
    candidate: CandidateProfileSchema,
    q: str,
    optimize_q: bool,
    location: str,
    max_results_per_source: int,
):
    raise NotImplemented()
