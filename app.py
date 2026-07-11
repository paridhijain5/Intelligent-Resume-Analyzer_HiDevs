"""Streamlit app for the Intelligent Resume Analyzer."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import streamlit as st

from matcher import ResumeMatcher
from report_generator import generate_hiring_report, save_report
from resume_parser import ResumeParser
from storage import load_json, save_json


DATA_DIR = Path("data")
RESULTS_DIR = DATA_DIR / "results"
SAVED_DATA_DIR = DATA_DIR / "saved"


def init_directories() -> None:
    """Create directories for storage and reports when needed."""
    for directory in (DATA_DIR, RESULTS_DIR, SAVED_DATA_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def load_saved_results() -> list[Dict[str, Any]]:
    """Load previously saved analysis results from disk."""
    items: list[Dict[str, Any]] = []
    if not SAVED_DATA_DIR.exists():
        return items
    for file_path in sorted(SAVED_DATA_DIR.glob("*.json")):
        try:
            data = load_json(file_path)
            items.append(data)
        except (FileNotFoundError, ValueError, RuntimeError):
            continue
    return items


def main() -> None:
    """Run the Streamlit app."""
    init_directories()
    st.set_page_config(page_title="Intelligent Resume Analyzer", page_icon="📄", layout="wide")
    st.title("Intelligent Resume Analyzer")
    st.write("Upload a resume and compare it with a job description to get a hiring recommendation.")

    uploaded_file = st.file_uploader("Upload Resume", type=["txt", "pdf", "docx"])
    job_description = st.text_area(
        "Job Description or Required Skills",
        height=220,
        placeholder="Example: Python, SQL, machine learning, AWS, Docker, teamwork",
    )

    col1, col2 = st.columns(2)
    with col1:
        analyze_button = st.button("Analyze Resume")
    with col2:
        save_result_button = st.button("Save Result")

    if analyze_button:
        try:
            if uploaded_file is None:
                st.error("Please upload a resume file before analyzing.")
                st.stop()
            if not job_description.strip():
                st.error("Please enter a job description or required skills.")
                st.stop()

            with st.spinner("Parsing resume and computing match..."):
                parser = ResumeParser()
                uploaded_name = Path(uploaded_file.name)
                tmp_path = DATA_DIR / uploaded_name.name
                tmp_path.parent.mkdir(parents=True, exist_ok=True)
                with tmp_path.open("wb") as handle:
                    handle.write(uploaded_file.getvalue())

                candidate_data = parser.parse_resume(tmp_path)

                matcher = ResumeMatcher()
                required_skills = matcher.extract_job_skills(job_description)
                if not required_skills:
                    required_skills = [skill.strip() for skill in job_description.split(",") if skill.strip()]
                match_result = matcher.compute_match(candidate_data["skills"], required_skills)

                report_text = generate_hiring_report(candidate_data, match_result)
                report_path = save_report(report_text, RESULTS_DIR / f"{candidate_data['candidate_name'].replace(' ', '_') or 'candidate'}_report.txt")
                candidate_data["match_result"] = match_result
                candidate_data["report_path"] = str(report_path)
                candidate_data["job_description"] = job_description

                st.session_state["candidate_data"] = candidate_data
                st.session_state["match_result"] = match_result
                st.session_state["report_text"] = report_text
                st.session_state["report_path"] = str(report_path)

            st.success("Analysis complete.")

            st.subheader("Candidate Summary")
            st.metric("Candidate Name", candidate_data.get("candidate_name", "Not found"))
            st.metric("Email", candidate_data.get("email", "Not found"))
            st.metric("Phone", candidate_data.get("phone_number", "Not found"))
            st.metric("Experience", candidate_data.get("years_of_experience", "Not found"))

            st.subheader("Skills")
            st.write(", ".join(candidate_data.get("skills", [])) or "No skills extracted")

            st.subheader("Match Result")
            score = match_result["score"]
            recommendation = match_result["recommendation"]
            st.metric("Match Score", f"{score}/100")
            st.metric("Recommendation", recommendation)

            st.write("Matched skills:")
            st.write(", ".join(match_result.get("matched_skills", [])) or "None")
            st.write("Missing skills:")
            st.write(", ".join(match_result.get("missing_skills", [])) or "None")

            st.download_button(
                label="Download Report",
                data=st.session_state["report_text"],
                file_name="hiring_report.txt",
                mime="text/plain",
            )

        except Exception as exc:  # pragma: no cover - UI surface for user-facing errors
            st.error(f"An error occurred: {exc}")

    if save_result_button:
        try:
            if "candidate_data" not in st.session_state:
                st.error("No analysis result is available to save yet.")
                st.stop()
            save_path = SAVED_DATA_DIR / f"{st.session_state['candidate_data']['candidate_name'].replace(' ', '_') or 'candidate'}_result.json"
            save_json(st.session_state["candidate_data"], save_path)
            st.success(f"Result saved to {save_path}")
        except Exception as exc:
            st.error(f"Unable to save result: {exc}")

    st.subheader("Previously Saved Results")
    saved_items = load_saved_results()
    if saved_items:
        for item in saved_items:
            st.write(f"- {item.get('candidate_name', 'Unknown')} | Score: {item.get('match_result', {}).get('score', 'N/A')}")
    else:
        st.info("No saved results yet.")


if __name__ == "__main__":
    main()
