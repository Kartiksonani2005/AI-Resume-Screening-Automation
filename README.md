# AI Resume Screening System

A Streamlit-based job application form connected to an n8n automation workflow.

## Tech Stack

- Python
- Streamlit
- n8n
- AI
- Google Drive
- Gmail
- Google Sheets

## Workflow

Candidate submits application and resume through Streamlit.

Streamlit sends the candidate information and PDF resume to an n8n webhook.

n8n processes the resume, performs AI-based screening, and stores/sends the results.