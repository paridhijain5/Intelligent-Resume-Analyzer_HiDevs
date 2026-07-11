# Intelligent Resume Analyzer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Project Overview

The **Intelligent Resume Analyzer** is a Python and Streamlit application that automates the initial resume-screening process.

It extracts important candidate information, compares resume skills with job requirements, calculates a match score, and generates a structured hiring recommendation. The project demonstrates practical use of Python programming, text processing, file handling, matching algorithms, and interactive application development.

## Features

- Upload resumes in TXT, PDF, or DOCX format
- Extract candidate name, email, phone number, skills, education, and experience
- Compare candidate skills with job requirements
- Calculate a resume match score from 0 to 100
- Display matched and missing skills
- Generate hiring recommendations
- Save and load analysis results in JSON format
- Download a professional candidate analysis report
- Handle missing, malformed, and unsupported input gracefully
- Interactive Streamlit user interface

## Hiring Recommendation Rules

| Match Score | Recommendation |
|---|---|
| 80–100 | Strong Match |
| 60–79 | Good Match |
| 40–59 | Partial Match |
| Below 40 | Not Recommended |

## Project Structure

```text
intelligent_resume_analyzer_hidevs/
│
├── app.py
├── resume_parser.py
├── matcher.py
├── report_generator.py
├── storage.py
├── utils.py
├── requirements.txt
├── README.md
│
├── data/
│   └── .gitkeep
│
└── sample_data/
    ├── sample_resume.txt
    └── sample_job_description.txt
```

## Technologies Used

- Python
- Streamlit
- PDFPlumber
- python-docx
- Pandas
- Scikit-learn
- Regular expressions
- JSON file handling

## Installation

### 1. Clone the repository

```bash
git clone [https://github.com/YOUR_USERNAME/intelligent_resume_analyzer_hidevs.git](https://github.com/paridhijain5/Intelligent-Resume-Analyzer_HiDevs)
cd intelligent_resume_analyzer_hidevs
```

### 2. Install the required packages

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How to Use

1. Upload a resume in TXT, PDF, or DOCX format.
2. Enter or paste the job description.
3. Click the **Analyze Resume** button.
4. Review the extracted candidate details.
5. Check the match score, matched skills, and missing skills.
6. Read the hiring recommendation.
7. Save the result or download the generated report.

## Matching Method

The application extracts skills from the candidate’s resume and compares them with the skills found in the job description.

A match percentage is generated using the proportion of required skills found in the resume:

```text
Match Score = Matched Required Skills / Total Required Skills × 100
```

The result is restricted to a range of 0 to 100.

## Error Handling

The application handles:

- Empty resume files
- Empty job descriptions
- Unsupported file formats
- Invalid or malformed email addresses
- Missing candidate information
- Files that cannot be read
- Missing skills or experience
- JSON saving and loading errors

Clear messages are displayed instead of allowing the program to crash.

## Demo

Watch the project demonstration:

[Demo Video](https://drive.google.com/file/d/1e_pjXx-gTCqtszEhQm-nLf3-DjodivYi/view?usp=sharing)

Try the live application:

[Open Streamlit App](https://intelligent-resume-analyzerhidevs-my8edzuh7ah9lvdt8fgltz.streamlit.app/)

## Sample Output

The generated analysis contains:

- Candidate name
- Email and phone number
- Extracted skills
- Experience information
- Match score
- Matched skills
- Missing skills
- Final hiring recommendation

## Limitations

- Resume extraction accuracy depends on the formatting and quality of the uploaded document.
- Skill matching is primarily based on keywords.
- Complex resume layouts may reduce parsing accuracy.
- The recommendation supports screening but should not replace human recruitment decisions.

## Future Improvements

- Add advanced NLP-based resume parsing
- Support batch resume processing
- Add candidate ranking
- Use semantic similarity for job matching
- Add visual dashboards
- Export reports in PDF format
- Add database integration
- Add authentication for recruiters


## Disclaimer

This application is an educational project. Hiring decisions should not be based solely on automated scores. Recruiters should review candidate qualifications independently.
