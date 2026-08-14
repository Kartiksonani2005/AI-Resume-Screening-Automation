import streamlit as st
import requests
import re
import os


# =========================
# Configuration
# =========================

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Resume Application",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Job Application")

st.write("Please fill in your details and upload your resume.")


# =========================
# Application Form
# =========================

with st.form("resume_form"):

    name = st.text_input("Candidate Name *")

    email = st.text_input("Email Address *")

    qualification = st.radio(
        "Qualification *",
        ["Bachelor's", "Master's"]
    )

    resume = st.file_uploader(
        "Upload Resume *",
        type=["pdf"]
    )

    submit = st.form_submit_button("Submit Application")


# =========================
# Form Submission
# =========================

if submit:

    # Validate name
    if not name.strip():

        st.error("Please enter your name.")

    # Validate email
    elif not email.strip():

        st.error("Please enter your email.")

    elif not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email
    ):

        st.error("Please enter a valid email address.")

    # Validate resume
    elif resume is None:

        st.error("Please upload your resume.")

    # Validate webhook configuration
    elif not WEBHOOK_URL:

        st.error("Application service is not configured.")

    else:

        # =========================
        # File Size Validation
        # =========================

        if resume.size > MAX_FILE_SIZE_BYTES:

            st.error(
                f"Resume file is too large. "
                f"Maximum allowed size is {MAX_FILE_SIZE_MB} MB."
            )

        else:

            with st.spinner("Submitting application..."):

                # =========================
                # Sanitize Filename
                # =========================

                safe_filename = re.sub(
                    r"[^a-zA-Z0-9._-]",
                    "_",
                    resume.name
                )

                # =========================
                # Prepare Resume File
                # =========================

                files = {
                    "resume": (
                        safe_filename,
                        resume.getvalue(),
                        "application/pdf"
                    )
                }

                # =========================
                # Candidate Information
                # =========================

                data = {
                    "candidate_name": name.strip(),
                    "candidate_email": email.strip(),
                    "qualification": qualification
                }

                try:

                    # =========================
                    # Send to n8n Webhook
                    # =========================

                    response = requests.post(
                        WEBHOOK_URL,
                        data=data,
                        files=files,
                        timeout=60
                    )

                    # =========================
                    # Handle Response
                    # =========================

                    if response.status_code == 200:

                        st.success(
                            "✅ Application submitted successfully!"
                        )

                    else:

                        st.error(
                            "❌ Unable to submit your application. "
                            "Please try again later."
                        )

                except requests.exceptions.Timeout:

                    st.error(
                        "⏱️ The application service took too long "
                        "to respond. Please try again."
                    )

                except requests.exceptions.RequestException:

                    st.error(
                        "❌ Unable to connect to the application service. "
                        "Please try again later."
                    )