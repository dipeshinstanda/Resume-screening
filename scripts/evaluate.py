import json
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
with open('data/sample_resumes.json', 'r') as f:
    resumes = json.load(f)

with open('data/sample_jobs.json', 'r') as f:
    jobs = json.load(f)

# Simulate ground truth (manual labels)
ground_truth = [
    {'resume_id': 1, 'job_id': 1},  # Match
    {'resume_id': 2, 'job_id': 2},  # Match
    {'resume_id': 3, 'job_id': 3},  # Match
    # No other matches
]

# Run screening
def screen_resumes(resumes, jobs):
    matches = []
    vectorizer = TfidfVectorizer()
    resume_texts = [' '.join(res['education']) for res in resumes]
    job_texts = [' '.join(job['required_education']) for job in jobs]
    all_texts = resume_texts + job_texts
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    for i, resume in enumerate(resumes):
        resume_vec = tfidf_matrix[i]
        for j, job in enumerate(jobs):
            job_vec = tfidf_matrix[len(resumes) + j]
            similarity = cosine_similarity(resume_vec, job_vec)[0][0]
            if similarity > 0.9:  # threshold
                matches.append({
                    'resume_id': resume['id'],
                    'job_id': job['id']
                })
    return matches

predictions = screen_resumes(resumes, jobs)

# Evaluate
all_pairs = [(r['id'], j['id']) for r in resumes for j in jobs]
y_true = [1 if {'resume_id': r, 'job_id': j} in ground_truth else 0 for r, j in all_pairs]
y_pred = [1 if {'resume_id': r, 'job_id': j} in predictions else 0 for r, j in all_pairs]

print(f'Accuracy: {accuracy_score(y_true, y_pred)}')
print(f'Precision: {precision_score(y_true, y_pred, zero_division=0)}')
print(f'Recall: {recall_score(y_true, y_pred, zero_division=0)}')
print(f'Predictions: {predictions}')