import re
import io
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TECH_SKILLS = [
    'python','java','javascript','typescript','c++','c#','go','rust','ruby','php',
    'swift','kotlin','scala','react','angular','vue','html','css','bootstrap',
    'tailwind','django','flask','fastapi','spring','express','nodejs',
    'mysql','postgresql','mongodb','redis','sqlite','elasticsearch',
    'aws','azure','gcp','docker','kubernetes','jenkins','linux','git',
    'machine learning','deep learning','tensorflow','pytorch','keras',
    'pandas','numpy','scikit-learn','nlp','sql','nosql','rest api',
    'graphql','microservices','agile','scrum','celery','kafka',
]

EDUCATION_KEYWORDS = ['bachelor','master','phd','b.sc','m.sc','b.tech','m.tech',
                      'mba','degree','university','college','institute']


def extract_text_from_pdf(file_obj):
    text = ''
    try:
        if hasattr(file_obj, 'read'):
            pdf_bytes = file_obj.read()
            file_obj.seek(0)
        else:
            with open(file_obj, 'rb') as f:
                pdf_bytes = f.read()
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    except Exception as e:
        text = ''
    return text


def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in TECH_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.append(skill)
    return list(set(found))


def extract_education(text):
    education = []
    for line in text.split('\n'):
        if any(kw in line.lower() for kw in EDUCATION_KEYWORDS):
            cleaned = line.strip()
            if len(cleaned) > 5:
                education.append(cleaned)
    return education[:5]


def extract_experience(text):
    experience = []
    patterns = [r'(\d+)\+?\s*years?\s+(?:of\s+)?experience', r'experience\s+of\s+(\d+)\+?\s*years?']
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            experience.append(f"{m.group(1)} years of experience")
            break
    keywords = ['engineer','developer','manager','analyst','intern','lead','architect','consultant']
    for line in text.split('\n'):
        if any(kw in line.lower() for kw in keywords):
            cleaned = line.strip()
            if 10 < len(cleaned) < 150:
                experience.append(cleaned)
    return experience[:8]


def calculate_match_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0, [], []
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        score = round(similarity * 100, 2)
    except Exception:
        score = 0.0
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))
    matched = list(resume_skills & jd_skills)
    missing = list(jd_skills - resume_skills)
    if jd_skills:
        score = min(100, score * 0.6 + (len(matched) / len(jd_skills)) * 40)
    return round(score, 2), matched, missing


def generate_suggestions(missing_skills, match_score):
    suggestions = []
    if match_score < 40:
        suggestions.append('Your resume needs significant improvement for this role.')
    elif match_score < 70:
        suggestions.append('Good start! Focus on the missing skills to improve your chances.')
    else:
        suggestions.append('Strong match! Minor improvements can make you a top candidate.')
    if missing_skills:
        suggestions.append(f"Priority skills to learn: {', '.join(missing_skills[:5])}")
    return suggestions
