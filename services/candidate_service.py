"""Candidate service for database operations.

This module provides functionality to query and persist candidate information
(including experiences, languages, skills, and qualifications) to the database.
"""

import logging
from sqlalchemy.orm import Session
from models.candidate import Candidate
from models.experience import Experience
from models.language import Language
from models.qualification import Qualification, QualificationField
from models.skill import Skill
from schemas.candidate import CandidateSchema

logger = logging.getLogger(__name__)


def get_candidate_by_hash(db: Session, content_hash: str) -> Candidate | None:
    """Retrieve a candidate by their resume content hash.

    Args:
        db: Database session.
        content_hash: Hash of the resume content.

    Returns:
        The Candidate object if found, None otherwise.
    """
    return db.query(Candidate).filter_by(content_hash=content_hash).first()


def _insert_candidate(
    db: Session, candidate_data: CandidateSchema, content_hash: str
) -> Candidate:
    """Insert a candidate and their related data into the database.

    Args:
        db: Database session.
        candidate_data: CandidateSchema containing candidate information
            along with experiences, languages, skills, and qualifications.
        content_hash: Hash of the resume content for deduplication.

    Returns:
        The inserted Candidate object with generated ID.
    """
    # Insert the candidate
    candidate = Candidate(
        **candidate_data.model_dump(
            exclude={"experiences", "languages", "qualifications", "skills"}
        ),
        content_hash=content_hash,
    )
    db.add(candidate)
    db.flush()

    # Insert the experiences
    db.add_all(
        [
            Experience(candidate_id=candidate.candidate_id, **exp.model_dump())
            for exp in candidate_data.experiences
        ]
    )

    # Insert the languages
    db.add_all(
        [
            Language(candidate_id=candidate.candidate_id, **lang.model_dump())
            for lang in candidate_data.languages
        ]
    )

    # Insert the skills
    db.add_all(
        [
            Skill(candidate_id=candidate.candidate_id, **skill.model_dump())
            for skill in candidate_data.skills
        ]
    )

    # Handle qualifications + their nested fields_of_study
    for qual in candidate_data.qualifications:
        qualification = Qualification(
            candidate_id=candidate.candidate_id,
            **qual.model_dump(exclude={"fields_of_study"}),
        )
        db.add(qualification)
        db.flush()

        db.add_all(
            [
                QualificationField(
                    qualification_id=qualification.qualification_id, field_id=field
                )
                for field in qual.fields_of_study
            ]
        )

    db.commit()
    db.refresh(candidate)

    return candidate


def upsert_candidate(
    db: Session, candidate_data: CandidateSchema, content_hash: str
) -> Candidate:
    """Insert or update a candidate in the database.

    If a candidate with the same email already exists, it will be replaced
    with the new data.

    Args:
        db: Database session.
        candidate_data: CandidateSchema containing candidate information.
        content_hash: Hash of the resume content for deduplication.

    Returns:
        The inserted Candidate object with generated ID.
    """
    existing = db.query(Candidate).filter_by(email=candidate_data.email).first()

    if existing:
        db.delete(existing)
        db.flush()  # delete before reinserting

    return _insert_candidate(db, candidate_data, content_hash)
