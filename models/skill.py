"""
This module defines the Skill model and the SkillProficiency enum.

Skill represents a skill a candidate has, along with their
proficiency level.
"""

import enum
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base


class SkillProficiency(enum.Enum):
    """Enumeration of skill proficiency levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Skill(Base):
    """Represents a skill that a candidate possesses.

    Attributes:
        skill_id: Primary key identifier.
        candidate_id: Foreign key to the candidate.
        name: Name of the skill (must be unique).
        proficiency: Candidate's proficiency level in the skill.
    """

    __tablename__ = "skill"

    skill_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.candidate_id"))
    name: Mapped[str] = mapped_column(unique=True)
    proficiency: Mapped[SkillProficiency | None] = mapped_column(Enum(SkillProficiency))
