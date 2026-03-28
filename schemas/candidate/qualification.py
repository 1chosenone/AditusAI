"""Pydantic schemas for qualification-related models."""

from pydantic import BaseModel
from enums import FieldOfStudyEnum, QualificationTypeEnum


class CandidateQualificationFieldSchema(BaseModel):
    field: FieldOfStudyEnum

    model_config = {"from_attributes": True}


class CandidateQualificationSchema(BaseModel):
    """Represents a candidate's qualification or credential.

    Attributes:
        institution: Name of the institution awarding the qualification.
        qualification_type: Type of qualification.
        description: Description of the qualification.
        start_year: Year the qualification started.
        end_year: Year the qualification was completed.
        fields: List of fields of study.
    """

    institution: str
    qualification_type: QualificationTypeEnum
    description: str | None = None
    start_year: int | None = None
    end_year: int
    fields: list[CandidateQualificationFieldSchema]

    model_config = {"from_attributes": True}
