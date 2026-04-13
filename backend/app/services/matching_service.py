from app.services.resume_service import ResumeService
from app.services.job_service import JobService
from app.models.ml_model import EducationMatcher

class MatchingService:
    def __init__(self):
        self.resume_service = ResumeService()
        self.job_service = JobService()
        self.matcher = EducationMatcher()
    
    def match_resumes_to_job(self, job_id, threshold=0.5):
        job = self.job_service.get_job_by_id(job_id)
        
        if not job:
            return {'error': 'Job not found'}
        
        resumes = self.resume_service.get_all_resumes()
        matches = []
        
        for resume in resumes:
            score = self.matcher.calculate_match_score(
                resume['education'],
                job.get('education_requirements', [])
            )
            
            if score >= threshold:
                matches.append({
                    'resume_id': resume['id'],
                    'filename': resume['filename'],
                    'score': score,
                    'education': resume['education']
                })
        
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'job_id': job_id,
            'job_title': job['title'],
            'total_matches': len(matches),
            'matches': matches
        }
    
    def calculate_match_score(self, resume_id, job_id):
        resume = self.resume_service.get_resume_by_id(resume_id)
        job = self.job_service.get_job_by_id(job_id)
        
        if not resume:
            return {'error': 'Resume not found'}
        if not job:
            return {'error': 'Job not found'}
        
        score = self.matcher.calculate_match_score(
            resume['education'],
            job.get('education_requirements', [])
        )
        
        return {
            'resume_id': resume_id,
            'job_id': job_id,
            'score': score
        }
