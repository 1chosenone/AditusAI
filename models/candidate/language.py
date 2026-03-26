"""
This module defines the Language model.

Language represents a language that a candidate knows, along with
their proficiency level.
"""

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.base import Base
from enums import LanguageProficiency


class CandidateLanguage(Base):
    """Represents a language that a candidate knows.

    Attributes:
        language_id: Primary key identifier.
        candidate_id: Foreign key to the candidate.
        name: Name of the language (must be unique).
        proficiency: Candidate's proficiency level in the language.
    """

    __tablename__ = "candidate_language"

    language_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate_profile.candidate_id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(unique=True)
    proficiency: Mapped[LanguageProficiency | None] = mapped_column(
        Enum(LanguageProficiency)
    )

    candidate: Mapped["CandidateProfile"] = relationship(back_populates="languages")
