"""Pydantic schemas for candidate-related models."""

from pydantic import BaseModel
from .experience import CandidateExperienceSchema
from .language import CandidateLanguageSchema
from .qualification import CandidateQualificationSchema
from .skill import CandidateSkillSchema


class CandidateProfileSchema(BaseModel):
    """Represents a job candidate or job seeker.

    Attributes:
        first_name: Candidate's first name.
        last_name: Candidate's last name.
        city: Candidate's city.
        region: Candidate's region (province, state, etc.).
        country: Candidate's country.
        email: Candidate's email address.
        phone: Candidate's phone number.
        bio: Short biography or summary.
        github_url: URL to the candidate's GitHub profile.
        linkedin_url: URL to the candidate's LinkedIn profile.
        experiences: List of work experiences.
        languages: List of languages known.
        skills: List of skills possessed.
    """

    first_name: str
    last_name: str
    city: str | None = None
    region: str | None = None
    country: str | None = None
    email: str | None = None
    phone: str | None = None
    bio: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    experiences: list[CandidateExperienceSchema] = []
    languages: list[CandidateLanguageSchema] = []
    qualifications: list[CandidateQualificationSchema] = []
    skills: list[CandidateSkillSchema] = []
