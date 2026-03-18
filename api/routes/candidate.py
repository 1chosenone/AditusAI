"""Candidate API routes."""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database.session import get_db
from core.queue import enqueue
from tasks.candidate import create_candidate_from_resume_task
from schemas.responses import CandidateResponse, JobResponse
from services.candidate_service import get_candidate_by_id

router = APIRouter(prefix="/candidate", tags=["candidate"])


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


@router.post("/resume")
async def create_candidate_from_resume(
    resume: UploadFile = File(..., description="PDF resume file to upload and parse")
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
