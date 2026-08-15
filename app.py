import streamlit as st
from PyPDF2 import PdfReader

from analyzer import (
    extract_skills,
    calculate_similarity,
    get_missing_skills,
    get_matching_skills,
    extract_keywords,
    generate_feedback
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📄 AI Resume Analyzer")

st.markdown(
    """
    ### Analyze your resume against a job description

    Upload your resume and paste a job description to get:
    
    - 🎯 Resume Match Score
    - 🛠️ Skills Found
    - ❌ Missing Skills
    - 🔑 Important Keywords
    - 💡 Resume Improvement Suggestions
    """
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        """
        AI Resume Analyzer helps students and job seekers
        understand how well their resume matches a particular
        job description.
        """
    )

    st.divider()

    st.subheader("Technology")

    st.write(
        """
        • Python  
        • Streamlit  
        • NLP  
        • TF-IDF  
        • Cosine Similarity  
        • PDF Processing
        """
    )


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"]
    )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder="Paste the complete job description..."
    )


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

analyze_button = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)


if analyze_button:

    if uploaded_file is None:

        st.error("Please upload your resume.")

        st.stop()


    if not job_description.strip():

        st.error("Please enter a job description.")

        st.stop()


    # --------------------------------------------------
    # EXTRACT PDF TEXT
    # --------------------------------------------------

    try:

        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text + "\n"

    except Exception as e:

        st.error("Could not read the PDF file.")

        st.stop()


    if not resume_text.strip():

        st.error(
            "No readable text was found in the PDF. "
            "Please upload a text-based PDF."
        )

        st.stop()


    # --------------------------------------------------
    # ANALYSIS
    # --------------------------------------------------

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    matching_skills = get_matching_skills(
        resume_skills,
        job_skills
    )

    missing_skills = get_missing_skills(
        resume_skills,
        job_skills
    )

    score = calculate_similarity(
        resume_text,
        job_description
    )

    keywords = extract_keywords(
        job_description
    )

    feedback = generate_feedback(
        score,
        missing_skills,
        matching_skills
    )


    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    st.divider()

    st.header("📊 Analysis Results")


    # SCORE

    score_col1, score_col2, score_col3 = st.columns(3)


    with score_col1:

        st.metric(
            "Resume Match Score",
            f"{score}%"
        )


    with score_col2:

        st.metric(
            "Matching Skills",
            len(matching_skills)
        )


    with score_col3:

        st.metric(
            "Missing Skills",
            len(missing_skills)
        )


    # --------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------

    st.subheader("🎯 Job Compatibility")

    st.progress(
        min(score / 100, 1.0)
    )


    # --------------------------------------------------
    # SKILLS
    # --------------------------------------------------

    skill_col1, skill_col2 = st.columns(2)


    with skill_col1:

        st.subheader("✅ Matching Skills")

        if matching_skills:

            for skill in matching_skills:

                st.success(skill)

        else:

            st.info(
                "No matching technical skills were detected."
            )


    with skill_col2:

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:

                st.warning(skill)

        else:

            st.success(
                "No missing skills detected from our skill database."
            )


    # --------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------

    st.subheader("🔑 Important Job Keywords")

    keyword_text = ", ".join(
        [word for word, count in keywords]
    )

    st.info(keyword_text)


    # --------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------

    st.subheader("💡 Resume Suggestions")

    for item in feedback:

        st.write(f"• {item}")


    # --------------------------------------------------
    # RESUME SKILLS
    # --------------------------------------------------

    st.subheader("🛠️ Skills Detected in Your Resume")

    if resume_skills:

        st.write(
            ", ".join(resume_skills)
        )

    else:

        st.warning(
            "No skills were detected from the current skill database."
        )


    # --------------------------------------------------
    # JOB SKILLS
    # --------------------------------------------------

    st.subheader("💼 Skills Detected in Job Description")

    if job_skills:

        st.write(
            ", ".join(job_skills)
        )

    else:

        st.warning(
            "No known skills were detected in the job description."
        )


    # --------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------

    st.divider()

    st.caption(
        "This tool provides an automated estimate and should not "
        "be considered professional recruitment advice."
    )