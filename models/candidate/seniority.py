"""Candidate seniority model."""

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.base import Base
from enums import SeniorityLevel


class CandidateSeniority(Base):
    """Represents a candidate's seniority level.

    Attributes:
        seniority_id: Primary key identifier.
        candidate_id: Foreign key to the candidate profile.
        level: Seniority level (e.g., Junior, Intermediate, Senior).
        years_of_experience: Candidate total years of experience
        candidate: Related candidate profile.
    """

    __tablename__ = "candidate_seniority"

    seniority_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate_profile.candidate_id", ondelete="CASCADE")
    )
    level: Mapped[SeniorityLevel] = mapped_column(Enum(SeniorityLevel))
    years_of_experience: Mapped[int] = mapped_column()

    candidate: Mapped["CandidateProfile"] = relationship(
        back_populates="seniority", uselist=False
    )
