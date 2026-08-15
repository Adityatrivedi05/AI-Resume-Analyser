import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills import SKILLS


def clean_text(text):
    """
    Convert text into lowercase and remove unnecessary characters.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text):
    """
    Find known technical skills inside the provided text.
    """
    text = clean_text(text)

    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_similarity(resume_text, job_description):
    """
    Calculate similarity between resume and job description
    using TF-IDF and cosine similarity.
    """

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    if not resume_text or not job_description:
        return 0

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def get_missing_skills(resume_skills, job_skills):
    """
    Find skills present in the job description
    but missing from the resume.
    """

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    return sorted(job_set - resume_set)


def get_matching_skills(resume_skills, job_skills):
    """
    Find skills appearing in both resume and job description.
    """

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    return sorted(resume_set.intersection(job_set))


def extract_keywords(text, top_n=15):
    """
    Extract frequently occurring words from text.
    """

    text = clean_text(text)

    words = re.findall(r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b", text)

    stop_words = {
        "the", "and", "for", "with", "this", "that",
        "from", "have", "has", "are", "you", "your",
        "will", "our", "they", "their", "into", "about",
        "job", "work", "years", "using"
    }

    words = [
        word for word in words
        if word not in stop_words
    ]

    counter = Counter(words)

    return counter.most_common(top_n)


def generate_feedback(score, missing_skills, matching_skills):
    """
    Generate simple rule-based resume feedback.
    """

    feedback = []

    if score >= 80:
        feedback.append(
            "Your resume has a strong match with this job description."
        )

    elif score >= 60:
        feedback.append(
            "Your resume has a good match, but some improvements are recommended."
        )

    elif score >= 40:
        feedback.append(
            "Your resume has a moderate match. Consider adding more relevant skills and keywords."
        )

    else:
        feedback.append(
            "Your resume has a low match with this job. Consider tailoring it for this position."
        )

    if missing_skills:
        feedback.append(
            "Consider highlighting relevant skills that you genuinely possess but have not mentioned clearly."
        )

    if len(matching_skills) < 3:
        feedback.append(
            "Try adding more relevant projects and technical keywords related to the target role."
        )

    feedback.append(
        "Use measurable achievements in your projects and experience sections where possible."
    )

    feedback.append(
        "Keep your resume concise, structured, and easy for recruiters to scan."
    )

    return feedback