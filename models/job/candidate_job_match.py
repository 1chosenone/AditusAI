"""Candidate-job matching data models."""

from sqlalchemy import CheckConstraint, ForeignKey, JSON, Text, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base


class CandidateJobMatch(Base):
    """Represents a match between a candidate and a job posting.

    Attributes:
        candidate_job_match_id: Primary key identifier.
        candidate_id: Foreign key to the candidate profile.
        job_id: Foreign key to the job posting.
        score: Match score (0.0 to 1.0).
        explication: Explanation of why this is a good match.
        matched_skills: List of skills the candidate has that match the job.
        missing_skills: List of skills the job requires but candidate lacks.
    """

    __tablename__ = "candidate_job_match"

    candidate_job_match_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate_profile.candidate_id", ondelete="CASCADE")
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("job_postings.job_id", ondelete="CASCADE")
    )

    score: Mapped[float] = mapped_column()
    explication: Mapped[str | None] = mapped_column(Text)

    matched_skills: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    missing_skills: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="unique_score_candidate_job"),
        CheckConstraint("score >= 0.0 AND score <= 1.0", name="check_score_range"),
    )
