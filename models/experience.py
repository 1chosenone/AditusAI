"""This module defines the Experience model and related enums.

Experience represents a candidate's work experience including
company, job title, industry, and employment dates.
"""

import enum

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped

from database.base import Base


class IndustryEnum(enum.Enum):
    """Enumeration of industry sectors."""

    AGRICULTURE = "Agriculture"
    MANUFACTURING = "Manufacturing"
    CONSTRUCTION = "Construction"
    ENERGY = "Energy"
    TRANSPORTATION = "Transportation"
    RETAIL = "Retail"
    WHOLESALE = "Wholesale"
    HOSPITALITY = "Hospitality"
    FOOD_BEVERAGE = "Food & Beverage"
    INFORMATION_TECHNOLOGY = "Information Technology"
    SOFTWARE = "Software"
    TELECOMMUNICATIONS = "Telecommunications"
    FINANCIAL_SERVICES = "Financial Services"
    BANKING = "Banking"
    INSURANCE = "Insurance"
    REAL_ESTATE = "Real Estate"
    HEALTHCARE = "Healthcare"
    PHARMACEUTICALS = "Pharmaceuticals"
    BIOTECHNOLOGY = "Biotechnology"
    EDUCATION = "Education"
    GOVERNMENT = "Government"
    NON_PROFIT = "Non-profit"
    MEDIA = "Media"
    ENTERTAINMENT = "Entertainment"
    PROFESSIONAL_SERVICES = "Professional Services"
    CONSULTING = "Consulting"
    LEGAL = "Legal"
    ENGINEERING = "Engineering"
    LOGISTICS = "Logistics"
    AUTOMOTIVE = "Automotive"
    AEROSPACE = "Aerospace"
    MINING = "Mining"
    CHEMICAL = "Chemical"
    AGRI_FOOD = "Agri-food"
    OTHER = "Other"


class JobTypeEnum(enum.Enum):
    """Enumeration of job types."""

    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    TEMPORARY = "Temporary"
    INTERNSHIP = "Internship"
    SEASONAL = "Seasonal"
    FREELANCE = "Freelance"


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
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.candidate_id"))
    company_name: Mapped[str] = mapped_column()
    job_title: Mapped[str] = mapped_column()
    job_type: Mapped[JobTypeEnum] = mapped_column(Enum(JobTypeEnum))
    industry: Mapped[IndustryEnum | None] = mapped_column(Enum(IndustryEnum))
    description: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column()
    region: Mapped[str | None] = mapped_column()
    country: Mapped[str | None] = mapped_column()
    start_year: Mapped[int] = mapped_column()
    end_year: Mapped[int | None] = mapped_column()
