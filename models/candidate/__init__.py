"""Candidate ORM classes representing the tables."""

from models.candidate.experience import CandidateExperience
from models.candidate.language import CandidateLanguage
from models.candidate.profile import CandidateProfile
from models.candidate.qualification import (
    CandidateQualification,
    CandidateQualificationField,
)
from models.candidate.skill import CandidateSkill

__all__ = [
    "CandidateExperience",
    "CandidateLanguage",
    "CandidateProfile",
    "CandidateQualification",
    "CandidateQualificationField",
    "CandidateSkill",
]
