"""Candidate service for database operations.

This module provides functionality to query and persist candidate information
(including experiences, languages, skills, and qualifications) to the database.
"""

import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from enums import SeniorityLevel
from exceptions import CandidateInsertError
from models.candidate import *
from schemas.candidate import CandidateProfileSchema
from schemas.candidate import CandidateExperienceSchema

logger = logging.getLogger(__name__)


def get_candidate_by_id(db: Session, candidate_id: int) -> Optional[CandidateProfile]:
    """Retrieve a candidate by their ID.

    Args:
        db: Database session.
        candidate_id: The candidate's unique identifier.

    Returns:
        The Candidate object if found, None otherwise.
    """

    return db.scalars(
        select(CandidateProfile)
        .where(CandidateProfile.candidate_id == candidate_id)
        .options(
            selectinload(CandidateProfile.experiences),
            selectinload(CandidateProfile.languages),
            selectinload(CandidateProfile.qualifications).selectinload(
                CandidateQualification.fields
            ),
            selectinload(CandidateProfile.seniority),
            selectinload(CandidateProfile.skills),
        )
    ).first()


def get_candidates(db: Session) -> list[CandidateProfile] | None:
    """Retrieve candidates from the db.

    Args:
        db: Database session.

    Returns:
        A list containing the Candidate objects if found, None otherwise.
    """
    return db.scalars(select(CandidateProfile)).all()


def get_candidate_by_hash(db: Session, content_hash: str) -> CandidateProfile | None:
    """Retrieve a candidate by their resume content hash.

    Args:
        db: Database session.
        content_hash: Hash of the resume content.

    Returns:
        The Candidate object if found, None otherwise.
    """
    return db.query(CandidateProfile).filter_by(content_hash=content_hash).first()


def _infer_seniority(
    experiences: list[CandidateExperienceSchema],
) -> tuple[SeniorityLevel, float]:
    """Infer seniority level based on work experience.

    Calculates total years of experience from all positions and determines
    the appropriate seniority level.

    Args:
        experiences: List of work experience entries.

    Returns:
        A tuple containing:
            - SeniorityLevel: JUNIOR (<3 years), MID (3-5 years), or SENIOR (>5 years)
            - float: Total years of experience
    """

    total_months = sum(
        (exp.end_year - exp.start_year) * 12 + (exp.end_month - exp.start_month)
        for exp in experiences
    )

    years_experience = total_months / 12

    if years_experience < 3:
        return SeniorityLevel.JUNIOR, years_experience
    if years_experience < 5:
        return SeniorityLevel.MID, years_experience

    return SeniorityLevel.SENIOR, years_experience


def _insert_candidate(
    db: Session, candidate_data: CandidateProfileSchema, content_hash: str
) -> CandidateProfile:
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
    candidate = CandidateProfile(
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
            CandidateExperience(candidate_id=candidate.candidate_id, **exp.model_dump())
            for exp in candidate_data.experiences
        ]
    )

    # Insert the languages
    db.add_all(
        [
            CandidateLanguage(candidate_id=candidate.candidate_id, **lang.model_dump())
            for lang in candidate_data.languages
        ]
    )

    # Insert the skills
    db.add_all(
        [
            CandidateSkill(candidate_id=candidate.candidate_id, **skill.model_dump())
            for skill in candidate_data.skills
        ]
    )

    # Insert seniority
    seniority_level, years_of_experience = _infer_seniority(candidate_data.experiences)
    db.add(
        CandidateSeniority(
            candidate_id=candidate.candidate_id,
            level=seniority_level,
            years_of_experience=years_of_experience,
        )
    )

    # Handle qualifications + their nested fields
    for qual in candidate_data.qualifications:
        qualification = CandidateQualification(
            candidate_id=candidate.candidate_id,
            **qual.model_dump(exclude={"fields"}),
        )
        db.add(qualification)
        db.flush()

        db.add_all(
            [
                CandidateQualificationField(
                    qualification_id=qualification.qualification_id, field=qf.field
                )
                for qf in qual.fields
            ]
        )

    db.commit()
    db.refresh(candidate)

    return candidate


def upsert_candidate(
    db: Session, candidate_data: CandidateProfileSchema, content_hash: str
) -> CandidateProfile:
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

    try:
        existing = (
            db.query(CandidateProfile).filter_by(email=candidate_data.email).first()
        )

        if existing:
            db.delete(existing)
            db.flush()  # delete before reinserting

    except Exception as e:
        raise CandidateInsertError("Unexpected error while inserting candidate") from e

    return _insert_candidate(db, candidate_data, content_hash)
