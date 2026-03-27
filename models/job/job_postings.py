"""Job posting data models."""

from sqlalchemy import Text
from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base


class JobPostings(Base):
    """Represents a job posting from various sources.

    Attributes:
        job_id: Primary key identifier.
        title: Job title or position.
        company: Company offering the position.
        source: Source platform (e.g., LinkedIn, Indeed).
        url: Unique URL to the job posting.
        location: Job location (city, remote, etc.).
        salary: Salary range (optional).
        job_type: Type of employment (full-time, contract, etc.).
        date: Date the job was posted.
        description: Full job description text.
    """

    __tablename__ = "job_postings"

    job_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    company: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str] = mapped_column()
    salary: Mapped[str | None] = mapped_column()
    job_type: Mapped[str | None] = mapped_column()
    date: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(Text)
