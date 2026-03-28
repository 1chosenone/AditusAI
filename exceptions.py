"""Custom exceptions for the AditusAI application."""


class ResumeParsingError(Exception):
    """Raised when the LLM fails to extract candidate info from a resume."""


class QueryOptimizationError(Exception):
    """Raised when the LLM fails to optimize a query provided by the user"""


class QueryTermsParsingError(Exception):
    """Raised when the LLM fails to correctly parse terms in the query provided by the user"""


class PDFExtractionError(Exception):
    """Raised when text extraction from a PDF fails."""


class CandidateInsertError(Exception):
    """Raised when an unexpected error occurs while inserting a candidate."""
