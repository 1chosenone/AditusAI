"""This module defines the Candidate model.

Candidate represents a job seeker with their personal information
and profile details.
"""

from sqlalchemy import Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.base import Base


class Candidate(Base):
    """Represents a job candidate or job seeker.

    Attributes:
        candidate_id: Primary key identifier.
        first_name: Candidate's first name.
        last_name: Candidate's last name.
        city: Candidate's city.
        region: Candidate's region (province, state, etc.).
        country: Candidate's country.
        email: Candidate's email address (unique).
        phone: Candidate's phone number.
        bio: Short biography or summary.
        github_url: URL to the candidate's GitHub profile.
        linkedin_url: URL to the candidate's LinkedIn profile.
    """

    __tablename__ = "candidate"
    candidate_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    city: Mapped[str | None] = mapped_column()
    region: Mapped[str | None] = mapped_column()
    country: Mapped[str | None] = mapped_column()
    email: Mapped[str | None] = mapped_column(unique=True)
    phone: Mapped[str | None] = mapped_column()
    bio: Mapped[str | None] = mapped_column(Text)
    github_url: Mapped[str | None] = mapped_column()
    linkedin_url: Mapped[str | None] = mapped_column()
    content_hash: Mapped[str | None] = mapped_column(unique=True)

    # Relationships with cascade delete
    experiences: Mapped[list["Experience"]] = relationship(
        "Experience",
        back_populates="candidate",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    languages: Mapped[list["Language"]] = relationship(
        "Language",
        back_populates="candidate",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        back_populates="candidate",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    qualifications: Mapped[list["Qualification"]] = relationship(
        "Qualification",
        back_populates="candidate",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
