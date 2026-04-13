import uuid
from datetime import datetime

class JobService:
    def __init__(self):
        self.jobs = {}
    
    def create_job(self, data):
        job_id = str(uuid.uuid4())
        job_data = {
            'id': job_id,
            'title': data['title'],
            'description': data['description'],
            'requirements': data['requirements'],
            'education_requirements': data.get('education_requirements', []),
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.jobs[job_id] = job_data
        return job_data
    
    def get_all_jobs(self):
        return list(self.jobs.values())
    
    def get_job_by_id(self, job_id):
        return self.jobs.get(job_id)
    
    def update_job(self, job_id, data):
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        job.update({
            'title': data.get('title', job['title']),
            'description': data.get('description', job['description']),
            'requirements': data.get('requirements', job['requirements']),
            'education_requirements': data.get('education_requirements', job['education_requirements']),
            'updated_at': datetime.now().isoformat()
        })
        
        return job
    
    def delete_job(self, job_id):
        if job_id in self.jobs:
            del self.jobs[job_id]
            return True
        return False
