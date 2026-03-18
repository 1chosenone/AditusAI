"""Pydantic schemas for PDF-related models."""

import hashlib
from pydantic import BaseModel, computed_field


class PDFContent(BaseModel):
    """Represents extracted content from a PDF resume.

    Attributes:
        text: Extracted text content from the PDF.
        hyperlinks: List of URLs found in the PDF.
    """

    text: str
    hyperlinks: list[str]

    @computed_field
    def content_hash(self) -> str:
        # Ensure deterministic ordering
        sorted_links = sorted(self.hyperlinks)

        combined = self.text + "|" + "|".join(sorted_links)

        return hashlib.sha256(combined.encode()).hexdigest()
