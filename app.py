import streamlit as st
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def extract_education(text):
    sentences = nltk.sent_tokenize(text)
    education_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'degree', 'diploma']
    education_sentences = [s for s in sentences if any(kw in s.lower() for kw in education_keywords)]
    return education_sentences

def match_education(resume_ed, job_ed):
    if not resume_ed or not job_ed:
        return 0.0
    vectorizer = TfidfVectorizer()
    texts = resume_ed + job_ed
    tfidf_matrix = vectorizer.fit_transform(texts)
    max_sim = 0
    for res_vec in tfidf_matrix[:len(resume_ed)]:
        for job_vec in tfidf_matrix[len(resume_ed):]:
            sim = cosine_similarity(res_vec, job_vec)[0][0]
            if sim > max_sim:
                max_sim = sim
    return max_sim

st.title("AI Resume Screening System")

st.header("Upload Resume and Enter Job Description")

uploaded_file = st.file_uploader("Upload Resume (TXT)", type="txt")
job_desc = st.text_area("Job Description")

if st.button("Analyze"):
    if uploaded_file is not None and job_desc:
        # Read resume
        resume_text = uploaded_file.read().decode("utf-8")
        
        # Extract education
        resume_ed = extract_education(resume_text)
        job_ed = extract_education(job_desc)
        
        st.subheader("Extracted Education from Resume:")
        st.write(resume_ed)
        
        st.subheader("Extracted Required Education from Job Description:")
        st.write(job_ed)
        
        # Match
        similarity = match_education(resume_ed, job_ed)
        
        st.subheader("Match Score:")
        st.write(f"Similarity: {similarity:.2f}")
        
        if similarity > 0.5:
            st.success("Potential Match!")
        else:
            st.warning("Not a strong match.")
    else:
        st.error("Please upload a resume and enter job description.")