"""Generate a professional hiring analysis report."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def generate_hiring_report(candidate_data: Dict[str, Any], match_result: Dict[str, Any]) -> str:
    """Build a readable text report for the hiring analysis."""
    candidate = candidate_data or {}
    match = match_result or {}

    matched_skills = ", ".join(match.get("matched_skills", [])) or "None"
    missing_skills = ", ".join(match.get("missing_skills", [])) or "None"
    skills = ", ".join(candidate.get("skills", [])) or "None"
    education = ", ".join(candidate.get("education", [])) or "None"

    report_lines = [
        "Intelligent Resume Analyzer - Hiring Report",
        "=" * 44,
        f"Candidate Name: {candidate.get('candidate_name', 'Not found')}",
        f"Email: {candidate.get('email', 'Not found')}",
        f"Phone Number: {candidate.get('phone_number', 'Not found')}",
        f"Years of Experience: {candidate.get('years_of_experience', 'Not found')}",
        f"Education: {education}",
        f"Extracted Skills: {skills}",
        f"Match Score: {match.get('score', 0)}/100",
        f"Recommendation: {match.get('recommendation', 'Not Recommended')}",
        f"Matched Skills: {matched_skills}",
        f"Missing Skills: {missing_skills}",
        "",
        "Summary:",
        "The candidate's profile was compared against the provided job requirements.",
        "The recommendation is based on the proportion of required skills that were found.",
    ]
    return "\n".join(report_lines)


def save_report(report_text: str, output_path: str | Path) -> Path:
    """Persist the generated report to a text file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_text, encoding="utf-8")
    return path
