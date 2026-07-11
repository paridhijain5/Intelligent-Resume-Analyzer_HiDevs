"""Matching logic for comparing candidate skills to job requirements."""

from __future__ import annotations

from typing import Any, Dict, List

from utils import extract_skills, normalize_skill


class ResumeMatcher:
    """Compute a transparent match score between candidate and job requirements."""

    def compute_match(self, candidate_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """Return matched skills, missing skills, score, and recommendation."""
        normalized_candidate = {normalize_skill(skill) for skill in candidate_skills if skill}
        normalized_required = [normalize_skill(skill) for skill in required_skills if skill]

        matched = sorted([skill for skill in normalized_required if skill in normalized_candidate])
        missing = sorted([skill for skill in normalized_required if skill not in normalized_candidate])

        if not normalized_required:
            score = 0
        else:
            score = min(100, max(0, round((len(matched) / len(normalized_required)) * 100)))

        return {
            "required_skills": normalized_required,
            "matched_skills": matched,
            "missing_skills": missing,
            "score": score,
            "recommendation": classify_recommendation(score),
        }

    def extract_job_skills(self, job_description: str) -> List[str]:
        """Parse a job description into a skill list using the same extraction logic."""
        return extract_skills(job_description)


def classify_recommendation(score: int) -> str:
    """Return a hiring recommendation string based on a score."""
    if score >= 80:
        return "Strong Match"
    if score >= 60:
        return "Good Match"
    if score >= 40:
        return "Partial Match"
    return "Not Recommended"
