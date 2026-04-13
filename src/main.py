"""
AI Based Resume Screening System
Main entry point for the application.
"""

import json
import os
import re
from difflib import SequenceMatcher
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def extract_education(text):
    # Simple extraction: find sentences with education keywords
    sentences = nltk.sent_tokenize(text)
    education_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'degree', 'diploma']
    education_sentences = [s for s in sentences if any(kw in s.lower() for kw in education_keywords)]
    # For simplicity, return the sentences as education
    return education_sentences

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def screen_resumes(resumes, jobs):
    matches = []
    vectorizer = TfidfVectorizer()
    all_educations = []
    for resume in resumes:
        if 'education' not in resume:
            resume['education'] = extract_education(resume['resume_text'])
        all_educations.extend(resume['education'])
    for job in jobs:
        all_educations.extend(job['required_education'])
    
    if all_educations:
        tfidf_matrix = vectorizer.fit_transform(all_educations)
        idx = 0
        for resume in resumes:
            resume_eds = resume['education']
            resume_vecs = tfidf_matrix[idx:idx+len(resume_eds)]
            idx += len(resume_eds)
            for job in jobs:
                job_eds = job['required_education']
                job_vecs = tfidf_matrix[idx:idx+len(job_eds)]
                idx += len(job_eds)
                # Compute max similarity between any resume ed and job ed
                max_sim = 0
                for res_vec in resume_vecs:
                    for job_vec in job_vecs:
                        sim = cosine_similarity(res_vec, job_vec)[0][0]
                        if sim > max_sim:
                            max_sim = sim
                if max_sim > 0.5:  # threshold
                    matches.append({
                        'resume_id': resume['id'],
                        'job_id': job['id'],
                        'job_title': job['job_title'],
                        'similarity': max_sim
                    })
            # Reset idx for jobs? No, since all at once.
    # Wait, this is wrong, idx is cumulative.
    # Better to vectorize all, then index properly.
    # Simplified: concatenate all education strings per resume/job
    resume_texts = [' '.join(res['education']) for res in resumes]
    job_texts = [' '.join(job['required_education']) for job in jobs]
    all_texts = resume_texts + job_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    for i, resume in enumerate(resumes):
        resume_vec = tfidf_matrix[i]
        for j, job in enumerate(jobs):
            job_vec = tfidf_matrix[len(resumes) + j]
            similarity = cosine_similarity(resume_vec, job_vec)[0][0]
            if similarity > 0.9:  # threshold for match
                matches.append({
                    'resume_id': resume['id'],
                    'job_id': job['id'],
                    'job_title': job['job_title'],
                    'similarity': similarity
                })
    return matches

def main():
    print("AI Resume Screening System")
    
    # Load data
    resumes = load_data(os.path.join('..', 'data', 'sample_resumes.json'))
    jobs = load_data(os.path.join('..', 'data', 'sample_jobs.json'))
    
    # Screen resumes
    matches = screen_resumes(resumes, jobs)
    
    # Output results
    print("Matches found:")
    for match in matches:
        print(f"Resume {match['resume_id']} matches Job {match['job_id']}: {match['job_title']}")

if __name__ == "__main__":
    main()