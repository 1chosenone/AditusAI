"""Pydantic schemas for skill-related models."""

from pydantic import BaseModel
from enums import SkillProficiency


class CandidateSkillSchema(BaseModel):
    """Represents a skill that a candidate possesses.

    Attributes:
        name: Name of the skill.
        proficiency: Candidate's proficiency level in the skill.
    """

    name: str
    proficiency: SkillProficiency | None = None
