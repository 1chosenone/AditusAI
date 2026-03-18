"""
This module defines the Skill model.

Skill represents a skill a candidate has, along with their
proficiency level.
"""

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.base import Base
from enums import SkillProficiency


class Skill(Base):
    """Represents a skill that a candidate possesses.

    Attributes:
        skill_id: Primary key identifier.
        candidate_id: Foreign key to the candidate.
        name: Name of the skill.
        proficiency: Candidate's proficiency level in the skill.
    """

    __tablename__ = "skill"

    skill_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate.candidate_id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column()
    proficiency: Mapped[SkillProficiency | None] = mapped_column(Enum(SkillProficiency))

    candidate: Mapped["Candidate"] = relationship(back_populates="skills")

    __table_args__ = (
        UniqueConstraint("candidate_id", "name", name="uq_skill_candidate_name"),
        # ↑ same candidate can't have Python twice, but two candidates can both have Python
    )
