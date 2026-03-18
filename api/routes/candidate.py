from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database.session import get_db
from exceptions import CandidateInsertError, PDFExtractionError, ResumeParsingError
from schemas.responses import CandidateResponse
from services.candidate_service import (
    get_candidate_by_id,
    get_candidate_by_hash,
    upsert_candidate,
)
from services.llm_service import extract_candidate_info
from utils.pdf_utils import save_pdf, extract_pdf_text

router = APIRouter(prefix="/candidate", tags=["candidate"])


@router.get("/{candidate_id}", response_model=CandidateResponse, tags=["candidate"])
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = get_candidate_by_id(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.post("/resume", response_model=CandidateResponse, tags=["candidate"])
async def create_candidate_from_resume(
    resume: UploadFile = File(..., description="PDF resume file to upload and parse"),
    db: Session = Depends(get_db),
):
    """Upload and parse a candidate resume PDF.

    Automatically extracts candidate information (name, skills, languages,
    qualifications) using AI. If a candidate with the same resume content
    already exists, returns the existing record (deduplication).

    Args:
        resume: PDF file containing the candidate's resume.
    Returns:
        CandidateResponse with extracted candidate information.
    """

    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=500, detail="The provided URL does not point to a PDF file."
        )

    try:
        save_pdf(resume.file, "resume.pdf")
    except:
        raise HTTPException(
            status_code=500, detail=f"Error uploading the resume '{resume.filename}'."
        )

    try:
        resume_content = extract_pdf_text("resume.pdf")
    except PDFExtractionError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Return early if resume hasn't changed
    existing = get_candidate_by_hash(db, resume_content.content_hash)
    if existing:
        return existing

    try:
        extracted_candidate_info = await extract_candidate_info(resume_content)
    except ResumeParsingError as e:
        raise HTTPException(status_code=422, detail=str(e))
    try:
        candidate = upsert_candidate(
            db, extracted_candidate_info, resume_content.content_hash
        )
    except CandidateInsertError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return candidate
