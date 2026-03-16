"""
This module defines the Language model and the LanguageProficiency enum.

Language represents a language that a candidate knows, along with
their proficiency level.
"""

import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base


class LanguageProficiency(enum.Enum):
    """Enumeration of language proficiency levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "advanced"
    PROFICIENT = "proficient"


class Language(Base):
    """Represents a language that a candidate knows.

    Attributes:
        language_id: Primary key identifier.
        candidate_id: Foreign key to the candidate.
        name: Name of the language (must be unique).
        proficiency: Candidate's proficiency level in the language.
    """

    __tablename__ = "language"

    language_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.candidate_id"))
    name: Mapped[str] = mapped_column(unique=True)
    proficiency: Mapped[LanguageProficiency | None] = mapped_column(
        Enum(LanguageProficiency)
    )
