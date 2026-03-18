"""Utilities for PDF processing."""

from io import TextIOWrapper
import logging
from pathlib import Path
import shutil
from pypdf import PdfReader, errors as pypdf_errors
from schemas.pdf import PDFContent

logger = logging.getLogger(__name__)


def extract_pdf_text(url: str) -> PDFContent:
    """Extract all text content and hyperlinks from a PDF file.

    Args:
        url: Path to the PDF file.

    Returns:
        PDFContent containing extracted text and hyperlinks.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the PDF file is invalid or corrupted.
        RuntimeError: If an unexpected error occurs while reading.
    """
    logger.debug("Extracting PDF text...")

    if not Path(url).exists():
        raise FileNotFoundError(f"PDF file not found: {url}")

    try:
        reader = PdfReader(url)
    except pypdf_errors.PdfReadError as e:
        raise ValueError(f"Invalid or corrupted PDF file: {url}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while reading PDF: {url}") from e

    text = ""
    hyperlinks = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if not page_text:
            logger.warning("Page %s has no extractable text", i + 1)
            continue

        text += page_text

        # Extract hyperlinks
        if "/Annots" in page:
            for annot in page["/Annots"]:
                annot_obj = annot.get_object()
                if annot_obj["/Subtype"] == "/Link":
                    if "/URI" in annot_obj["/A"]:
                        uri = annot_obj["/A"]["/URI"]
                        logger.debug(
                            "%s url extracted from page %s of the PDF",
                            uri,
                            i + 1,
                        )
                        hyperlinks.append(uri)

    logger.info(
        "Finished extracting text from PDF '%s' (%s pages)", url, len(reader.pages)
    )
    return PDFContent(text=text, hyperlinks=hyperlinks)


def save_pdf(file: TextIOWrapper, save_path: str):
    """Save an uploaded PDF file to disk.

    Args:
        file: Uploaded file object.
        save_path: Destination file path.
    """
    logger.debug("Saving PDF file at %s...", save_path)

    destination = Path(save_path)

    if not destination.parent.exists():
        raise FileNotFoundError(
            f"Destination directory does not exist: {destination.parent}"
        )

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)
    except OSError:
        logger.exception("Failed to save PDF to %s", save_path)
        raise

    logger.info("PDF file saved at %s", save_path)
