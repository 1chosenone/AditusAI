"""This module defines the Experience model.

Experience represents a candidate's work experience including
company, job title, industry, and employment dates.
"""

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.base import Base
from enums import IndustryEnum, JobTypeEnum


class Experience(Base):
    """Represents a candidate's work experience.

    Attributes:
        experience_id: Primary key identifier.
        candidate_id: Foreign key to the candidate.
        company_name: Name of the company.
        job_title: Title of the position.
        job_type: Type of employment (e.g., Full-time, Part-time).
        industry: Industry sector of the experience.
        description: Description of responsibilities and achievements.
        city: City where the job was located.
        region: Region (province, state, etc.) where the job was located.
        country: Country where the job was located.
        start_year: Year the position started.
        end_year: Year the position ended (None if current).
    """

    __tablename__ = "experience"

    experience_id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidate_profile.candidate_id", ondelete="CASCADE")
    )
    company_name: Mapped[str] = mapped_column()
    job_title: Mapped[str] = mapped_column()
    job_type: Mapped[JobTypeEnum | None] = mapped_column(Enum(JobTypeEnum))
    industry: Mapped[IndustryEnum | None] = mapped_column(Enum(IndustryEnum))
    description: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column()
    region: Mapped[str | None] = mapped_column()
    country: Mapped[str | None] = mapped_column()
    start_year: Mapped[int] = mapped_column()
    end_year: Mapped[int | None] = mapped_column()

    candidate: Mapped["CandidateProfile"] = relationship(back_populates="experiences")
