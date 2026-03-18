"""Pydantic schemas for qualification-related models."""

from pydantic import BaseModel
from enums import FieldOfStudyEnum, QualificationTypeEnum


class QualificationSchema(BaseModel):
    """Represents a candidate's qualification or credential.

    Attributes:
        institution: Name of the institution awarding the qualification.
        qualification_type: Type of qualification.
        description: Description of the qualification.
        start_year: Year the qualification started.
        end_year: Year the qualification was completed.
        fields_of_study: List of fields of study.
    """

    institution: str
    qualification_type: QualificationTypeEnum
    description: str | None = None
    start_year: int | None = None
    end_year: int
    fields_of_study: list[FieldOfStudyEnum] = []
