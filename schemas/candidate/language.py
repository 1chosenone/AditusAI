"""Pydantic schemas for language-related models."""

from pydantic import BaseModel
from enums import LanguageProficiency


class CandidateLanguageSchema(BaseModel):
    """Represents a language that a candidate knows.

    Attributes:
        name: Name of the language.
        proficiency: Candidate's proficiency level in the language.
    """

    name: str
    proficiency: LanguageProficiency | None = None
