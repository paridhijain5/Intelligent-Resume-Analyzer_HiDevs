"""Resume parsing helpers for TXT, PDF, and DOCX files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pdfplumber
from docx import Document

from utils import (
    clean_text,
    extract_education,
    extract_email,
    extract_name,
    extract_phone,
    extract_skills,
    extract_years_experience,
    normalize_text,
)


class ResumeParser:
    """Parse resumes from common document formats."""

    def parse_resume(self, file_path: str | Path) -> Dict[str, Any]:
        """Parse a supported resume file and return structured candidate data."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {path}")

        suffix = path.suffix.lower()
        if suffix == ".txt":
            text = self._read_text_file(path)
        elif suffix == ".pdf":
            text = self._read_pdf_file(path)
        elif suffix == ".docx":
            text = self._read_docx_file(path)
        else:
            raise ValueError("Unsupported file type. Please upload a .txt, .pdf, or .docx resume.")

        return self._parse_text(text, file_name=path.name)

    def _read_text_file(self, path: Path) -> str:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            return handle.read()

    def _read_pdf_file(self, path: Path) -> str:
        text_chunks: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text_chunks.append(page.extract_text() or "")
        return "\n".join(text_chunks)

    def _read_docx_file(self, path: Path) -> str:
        document = Document(path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        return "\n".join(paragraphs)

    def _parse_text(self, text: str, file_name: str) -> Dict[str, Any]:
        cleaned_text = clean_text(text)
        normalized_text = normalize_text(cleaned_text)

        candidate_data = {
            "file_name": file_name,
            "candidate_name": extract_name(cleaned_text),
            "email": extract_email(cleaned_text),
            "phone_number": extract_phone(cleaned_text),
            "skills": extract_skills(cleaned_text),
            "years_of_experience": extract_years_experience(cleaned_text),
            "education": extract_education(cleaned_text),
            "raw_text_preview": cleaned_text[:800],
            "source_text": normalized_text,
        }
        return candidate_data
