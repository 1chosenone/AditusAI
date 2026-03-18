"""Pydantic schemas for PDF-related models."""

from pydantic import BaseModel


class PDFContent(BaseModel):
    """Represents extracted content from a PDF resume.

    Attributes:
        text: Extracted text content from the PDF.
        hyperlinks: List of URLs found in the PDF.
    """

    text: str
    hyperlinks: list[str]
