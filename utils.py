"""Utility helpers for text cleaning and extraction."""

from __future__ import annotations

import re
from typing import List

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}")

COMMON_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "html",
    "css",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "aws",
    "docker",
    "kubernetes",
    "git",
    "linux",
    "pandas",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "data analysis",
    "excel",
    "tableau",
    "power bi",
    "spark",
    "hadoop",
    "rest api",
    "flask",
    "django",
    "streamlit",
    "pytest",
]


def normalize_text(text: str) -> str:
    """Collapse overly spaced text into a readable single-line format."""
    return re.sub(r"\s+", " ", text or "").strip()


def clean_text(text: str) -> str:
    """Return a normalized string with line breaks preserved for parsing."""
    return re.sub(r"\r\n?", "\n", text or "").strip()


def normalize_skill(skill: str) -> str:
    """Normalize a skill label so matching is case-insensitive."""
    return re.sub(r"\s+", " ", skill.strip().lower())


def extract_email(text: str) -> str:
    """Extract the first email address found in the provided text."""
    match = EMAIL_PATTERN.search(text or "")
    return match.group(0) if match else "Not found"


def extract_phone(text: str) -> str:
    """Extract the first phone number found in the provided text."""
    match = PHONE_PATTERN.search(text or "")
    return match.group(0) if match else "Not found"


def extract_name(text: str) -> str:
    """Best-effort name extraction from the first few lines of the resume."""
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    for line in lines[:8]:
        if EMAIL_PATTERN.search(line) or PHONE_PATTERN.search(line):
            continue
        if len(line.split()) <= 4 and re.match(r"^[A-Z][A-Za-z .'-]+$", line):
            return line
    return "Not found"


def extract_years_experience(text: str) -> str:
    """Extract experience as a human-readable string when possible."""
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+experience)?",
        r"(\d+)\s*(?:years?|yrs?)\s*(?:of\s+experience)?",
        r"(?:since|from)\s*(\d{4})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            if pattern.endswith(r"(\d{4})"):
                return f"Since {match.group(1)}"
            value = match.group(1)
            return f"{value} years"
    return "Not found"


def extract_education(text: str) -> List[str]:
    """Extract education-related lines using basic patterns."""
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    education_terms = ["bachelor", "master", "phd", "diploma", "degree", "university", "college", "school"]
    found: List[str] = []
    for line in lines:
        lower_line = line.lower()
        if any(term in lower_line for term in education_terms):
            found.append(line)
    return found if found else ["Not found"]


def extract_skills(text: str, skill_names: List[str] | None = None) -> List[str]:
    """Extract known skills from text using case-insensitive regex matching."""
    skill_list = skill_names or COMMON_SKILLS
    found: List[str] = []
    lowered_text = (text or "").lower()
    for skill in sorted(skill_list, key=len, reverse=True):
        pattern = re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)
        if pattern.search(lowered_text):
            found.append(skill)
    return sorted(found)
