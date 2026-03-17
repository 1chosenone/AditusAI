"""
This module defines the Skill model.

Skill represents a skill a candidate has, along with their
proficiency level.
"""

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base
from enums import SkillProficiency


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
