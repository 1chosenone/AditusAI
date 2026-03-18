"""Background tasks for candidate processing."""

import asyncio
from database.session import SESSION_LOCAL
from services.candidate_service import get_candidate_by_hash, upsert_candidate
from services.llm_service import extract_candidate_info
from utils.pdf_utils import save_pdf, extract_pdf_text


def create_candidate_from_resume_task(resume) -> dict[str, int]:
    """Process a resume and create or update a candidate record.

    Saves the uploaded PDF, extracts text content, checks for existing
    candidate by content hash (deduplication), then uses AI to extract
    candidate information and persists to the database.

    Args:
        resume: Uploaded PDF file object.

    Returns:
        dict with candidate_id of the created or existing candidate.
    """
    save_pdf(resume.file, "resume.pdf")

    resume_content = extract_pdf_text("resume.pdf")

    with SESSION_LOCAL() as db:
        # Return early if resume hasn't changed
        existing = get_candidate_by_hash(db, resume_content.content_hash)
        if existing:
            return {"candidate_id": existing.candidate_id}

        extracted_candidate_info = asyncio.run(extract_candidate_info(resume_content))

        candidate = upsert_candidate(
            db, extracted_candidate_info, resume_content.content_hash
        )

        return {"candidate_id": candidate.candidate_id}
