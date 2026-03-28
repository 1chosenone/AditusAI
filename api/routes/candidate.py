"""Candidate API routes."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from database.session import get_db
from core.queue import enqueue
from tasks.candidate import create_candidate_from_resume_task
from tasks.jobs import discover_jobs
from schemas.responses import CandidateResponse, JobResponse
from services.candidate_service import get_candidate_by_id, get_candidates

router = APIRouter(prefix="/candidates", tags=["candidate"])


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Retrieve a candidate by their ID.

    Args:
        candidate_id: The candidate's unique identifier.
        db: Database session.

    Returns:
        CandidateResponse with the candidate's information.

    Raises:
        HTTPException: 404 if candidate is not found.
    """
    candidate = get_candidate_by_id(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.get("", response_model=list[CandidateResponse])
def get_candidate(db: Session = Depends(get_db)):
    """Retrieve all the candidates.

    Args:
        db: Database session.

    Returns:
        List of CandidateResponse with all the candidates information.
    """
    candidates = get_candidates(db)
    return candidates


@router.post("/resume", response_model=JobResponse)
def create_candidate_from_resume(
    resume: UploadFile = File(..., description="PDF resume file to upload and parse"),
):
    """Upload and parse a candidate resume PDF.

    Enqueues a background task to extract candidate information (name,
    skills, languages, qualifications) from the resume using AI.
    Returns a job ID to track the processing status.

    Args:
        resume: PDF file containing the candidate's resume.
        db: Database session.

    Returns:
        dict with job_id to track the background task.

    Raises:
        HTTPException: 415 if the file is not a PDF.
    """
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail=f"Invalid file type '{resume.content_type}'. Only PDF files are accepted.",
        )

    job_id = enqueue(create_candidate_from_resume_task, resume)
    return JobResponse(job_id=job_id)


@router.post("/{candidate_id}/job-discovery", response_model=JobResponse)
def fetch_jobs_for_candidate(
    candidate_id: int,
    q: Optional[str] = Query(
        None, description="Search keyword, e.g. 'ai' or 'fullstack developer'"
    ),
    optimize_q: bool = Query(
        False, description="Use candidate profile to optimize the search query"
    ),
    location: Optional[str] = Query(None, description="Filter by location"),
    max_results_per_source: int = Query(
        10,
        ge=1,
        le=50,
        description="Maximum number of results to fetch per job platform (e.g. LinkedIn, Indeed)",
    ),
    db: Session = Depends(get_db),
):
    """Discover and fetch matching jobs for a candidate.

    Enqueues a background task to search for jobs based on the provided
    criteria and candidate profile. Returns a job ID to track processing.

    Args:
        candidate_id: The candidate's unique identifier.
        q: Optional search keyword for job titles or descriptions.
        optimize_q: Whether to optimize `q` the search query using
            the candidate's profile information.
        location: Filter jobs by location (city, remote, etc.).
        max_results_per_source: Maximum results to fetch from each platform.

    Returns:
        JobResponse with job_id to track the background task.

    Raises:
        HTTPException: 404 if candidate is not found.
    """
    candidate = CandidateResponse.model_validate(get_candidate_by_id(db, candidate_id))
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    job_id = enqueue(
        discover_jobs, candidate, q, optimize_q, location, max_results_per_source
    )
    return JobResponse(job_id=job_id)
