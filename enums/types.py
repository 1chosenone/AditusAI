"""Enumerations used throughout the AditusAI application."""

import enum


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


class LanguageProficiency(enum.Enum):
    """Enumeration of language proficiency levels."""

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    PROFICIENT = "Proficient"


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


class SkillProficiency(enum.Enum):
    """Enumeration of skill proficiency levels."""

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class SeniorityLevel(enum.Enum):
    """Enumeration of seniority levels."""

    JUNIOR = "Junior"
    MID = "Mid"
    SENIOR = "Senior"
