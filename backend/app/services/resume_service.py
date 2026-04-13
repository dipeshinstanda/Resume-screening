import uuid
from datetime import datetime

from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.docx_parser import extract_text_from_docx
from app.utils.education_extractor import extract_education

class ResumeService:
    def __init__(self):
        self.resumes = {}
    
    def process_resume(self, filepath, filename):
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(filepath)
        else:
            return {'error': 'Unsupported file format'}
        
        education = extract_education(text)
        
        resume_id = str(uuid.uuid4())
        resume_data = {
            'id': resume_id,
            'filename': filename,
            'text': text,
            'education': education,
            'uploaded_at': datetime.now().isoformat(),
            'status': 'processed'
        }
        
        self.resumes[resume_id] = resume_data
        
        return {
            'id': resume_id,
            'filename': filename,
            'education': education,
            'message': 'Resume processed successfully'
        }
    
    def get_all_resumes(self):
        return list(self.resumes.values())
    
    def get_resume_by_id(self, resume_id):
        return self.resumes.get(resume_id)
    
    def delete_resume(self, resume_id):
        if resume_id in self.resumes:
            del self.resumes[resume_id]
            return True
        return False
