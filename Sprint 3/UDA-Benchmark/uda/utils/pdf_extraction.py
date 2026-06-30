"""
PDF extraction utilities using pdfplumber for better table handling.

Created: June 29, 2026
Purpose: Replace PyPDF2 to fix table extraction issues in Phase 3A
Author: UDA Benchmark Team

Improvements over PyPDF2:
- Tables are preserved with proper structure
- Numbers are not scrambled
- Better spacing and formatting
- Explicit page and table markers for better chunking
"""

import pdfplumber
import PyPDF2
from pathlib import Path
from typing import Optional


def extract_text_pdfplumber(pdf_path: str) -> str:
    """
    Extract text from PDF using pdfplumber for better table handling.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text with tables properly formatted

    Features:
        - Preserves table structure with | separators
        - Adds page markers for better context
        - Adds header row separators
        - Handles empty cells gracefully
    """
    text_parts = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract regular text
                page_text = page.extract_text() or ""

                # Extract tables
                tables = page.extract_tables()

                if tables:
                    # Add page header
                    text_parts.append(f"\n{'='*80}\n")
                    text_parts.append(f"PAGE {page_num}\n")
                    text_parts.append(f"{'='*80}\n\n")

                    # Add text content before tables
                    if page_text.strip():
                        text_parts.append(f"[TEXT CONTENT]\n{page_text}\n\n")

                    # Add formatted tables
                    for table_idx, table in enumerate(tables, 1):
                        text_parts.append(f"[TABLE {table_idx}]\n")

                        # Convert table to formatted text
                        for row_idx, row in enumerate(table):
                            # Clean cells and join with separator
                            clean_row = [str(cell or "").strip() for cell in row]

                            # Use | separator for better parsing
                            row_text = " | ".join(clean_row)
                            text_parts.append(f"{row_text}\n")

                            # Add separator after header row (first row)
                            if row_idx == 0:
                                separator = "-" * len(row_text)
                                text_parts.append(f"{separator}\n")

                        text_parts.append("\n")
                else:
                    # No tables, just add text with page marker
                    text_parts.append(f"\n{'='*80}\n")
                    text_parts.append(f"PAGE {page_num}\n")
                    text_parts.append(f"{'='*80}\n\n")
                    text_parts.append(f"{page_text}\n\n")

        return "".join(text_parts)

    except Exception as e:
        raise RuntimeError(f"pdfplumber extraction failed for {pdf_path}: {e}")


def extract_text_pypdf2(pdf_path: str) -> str:
    """
    Extract text using PyPDF2 (fallback method).

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text (basic, no table structure)
    """
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f, strict=False)
            text_parts = []

            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text_parts.append(f"\n{'='*80}\n")
                text_parts.append(f"PAGE {page_num}\n")
                text_parts.append(f"{'='*80}\n\n")
                text_parts.append(f"{page_text}\n\n")

            return "".join(text_parts)

    except Exception as e:
        raise RuntimeError(f"PyPDF2 extraction failed for {pdf_path}: {e}")


def extract_text_hybrid(pdf_path: str, prefer_pdfplumber: bool = True) -> str:
    """
    Hybrid extraction: Try pdfplumber first, fall back to PyPDF2.

    Args:
        pdf_path: Path to PDF file
        prefer_pdfplumber: If True, use pdfplumber; if False, use PyPDF2

    Returns:
        Extracted text

    Usage in notebooks:
        # For table-heavy PDFs (recommended)
        text = extract_text_hybrid(pdf_path, prefer_pdfplumber=True)

        # For text-only PDFs (faster)
        text = extract_text_hybrid(pdf_path, prefer_pdfplumber=False)
    """
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if prefer_pdfplumber:
        try:
            print(f"📄 Extracting with pdfplumber: {Path(pdf_path).name}")
            return extract_text_pdfplumber(pdf_path)
        except Exception as e:
            print(f"⚠️  pdfplumber failed ({e}), falling back to PyPDF2")
            return extract_text_pypdf2(pdf_path)
    else:
        try:
            print(f"📄 Extracting with PyPDF2: {Path(pdf_path).name}")
            return extract_text_pypdf2(pdf_path)
        except Exception as e:
            print(f"⚠️  PyPDF2 failed ({e}), trying pdfplumber")
            return extract_text_pdfplumber(pdf_path)


# Convenience function - default to pdfplumber
def extract_pdf_text(pdf_path: str) -> str:
    """
    Main extraction function - uses pdfplumber by default.

    Drop-in replacement for old extract_pdf_text function in notebooks.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text with proper table formatting

    Example:
        >>> from uda.utils.pdf_extraction import extract_pdf_text
        >>> text = extract_pdf_text("path/to/document.pdf")
        >>> print(text[:500])  # First 500 chars
    """
    return extract_text_hybrid(pdf_path, prefer_pdfplumber=True)


if __name__ == "__main__":
    # Quick test if run directly
    import sys

    if len(sys.argv) > 1:
        test_pdf = sys.argv[1]
        print(f"Testing extraction on: {test_pdf}")
        print("="*80)

        try:
            text = extract_pdf_text(test_pdf)
            print(f"\n✅ Extraction successful!")
            print(f"Total length: {len(text)} characters")
            print(f"\nFirst 500 characters:")
            print("-"*80)
            print(text[:500])
        except Exception as e:
            print(f"\n❌ Extraction failed: {e}")
    else:
        print("Usage: python3 pdf_extraction.py <path_to_pdf>")
        print("\nThis module provides pdfplumber-based PDF extraction.")
        print("Import in notebooks: from uda.utils.pdf_extraction import extract_pdf_text")
