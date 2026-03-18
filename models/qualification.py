"""
This module defines the Qualification model.

Qualification represents a candidate's educational qualifications,
certifications, and credentials along with their field of study.
"""

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base
from enums import FieldOfStudyEnum, QualificationTypeEnum


class Qualification(Base):
    """Represents a candidate's qualification or credential.

    Attributes:
        qualification_id: Primary key identifier.
        candidate_id: Foreign key to the candidate.
        institution: Name of the institution awarding the qualification.
        qualification_type: Type of qualification (e.g., Bachelor, Master).
        description: Description of the qualification.
        start_year: Year the qualification started.
        end_year: Year the qualification was completed.
    """

    __tablename__ = "qualification"

    qualification_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.candidate_id"))
    institution: Mapped[str] = mapped_column()
    qualification_type: Mapped[QualificationTypeEnum] = mapped_column(
        Enum(QualificationTypeEnum)
    )
    description: Mapped[str | None] = mapped_column(Text)
    start_year: Mapped[int | None] = mapped_column()
    end_year: Mapped[int] = mapped_column()


class QualificationField(Base):
    """Represents the field of study for a qualification.

    Attributes:
        qualification_id: Foreign key to the qualification.
        field_id: Field of study enum value.
    """

    __tablename__ = "qualification_field"
    qualification_id: Mapped[int] = mapped_column(
        ForeignKey("qualification.qualification_id"),
        primary_key=True,
    )
    field_id: Mapped[FieldOfStudyEnum] = mapped_column(
        Enum(FieldOfStudyEnum), primary_key=True
    )
