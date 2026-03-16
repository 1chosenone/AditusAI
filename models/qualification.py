"""
This module defines the Qualification model and related enums.

Qualification represents a candidate's educational qualifications,
certifications, and credentials along with their field of study.
"""

import enum
from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base


class QualificationTypeEnum(enum.Enum):
    """
    Enum representing different types of candidate qualifications or credentials.
    """

    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORAL = "Doctoral"
    DIPLOMA = "Diploma"
    CERTIFICATION = "Certification"
    LICENSE = "License"
    AWARD = "Award"
    OTHER = "Other"


class FieldOfStudyEnum(enum.Enum):
    """
    Enum representing various fields of study or disciplines for candidate qualifications.
    """

    COMPUTER_SCIENCE = "Computer Science"
    INFORMATION_TECHNOLOGY = "Information Technology"
    ENGINEERING = "Engineering"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    CIVIL_ENGINEERING = "Civil Engineering"
    BUSINESS_ADMINISTRATION = "Business Administration"
    FINANCE = "Finance"
    ACCOUNTING = "Accounting"
    MARKETING = "Marketing"
    ECONOMICS = "Economics"
    LAW = "Law"
    MEDICINE = "Medicine"
    NURSING = "Nursing"
    PHARMACY = "Pharmacy"
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"
    MATHEMATICS = "Mathematics"
    PSYCHOLOGY = "Psychology"
    EDUCATION = "Education"
    SOCIAL_SCIENCES = "Social Sciences"
    ARTS = "Arts"
    MUSIC = "Music"
    HISTORY = "History"
    LITERATURE = "Literature"
    LANGUAGE_STUDIES = "Language Studies"
    ENVIRONMENTAL_SCIENCE = "Environmental Science"
    OTHER = "Other"


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
        ForeignKey("qualification.qualification_id", primary_key=True)
    )
    field_id: Mapped[FieldOfStudyEnum] = mapped_column(
        Enum(FieldOfStudyEnum), primary_key=True
    )
