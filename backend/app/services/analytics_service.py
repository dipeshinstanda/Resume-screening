from app.services.resume_service import ResumeService
from app.services.job_service import JobService

class AnalyticsService:
    def __init__(self):
        self.resume_service = ResumeService()
        self.job_service = JobService()
    
    def get_system_metrics(self):
        resumes = self.resume_service.get_all_resumes()
        jobs = self.job_service.get_all_jobs()
        
        return {
            'total_resumes': len(resumes),
            'total_jobs': len(jobs),
            'processed_resumes': len([r for r in resumes if r['status'] == 'processed']),
            'active_jobs': len([j for j in jobs if j['status'] == 'active'])
        }
    
    def get_performance_metrics(self):
        return {
            'accuracy': 0.0,
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'note': 'Performance metrics will be calculated after model training and validation'
        }
