from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

from app.services.resume_service import ResumeService

resume_bp = Blueprint('resume', __name__)
resume_service = ResumeService()

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    
    result = resume_service.process_resume(filepath, filename)
    
    return jsonify(result), 201

@resume_bp.route('', methods=['GET'])
def get_resumes():
    resumes = resume_service.get_all_resumes()
    return jsonify(resumes), 200

@resume_bp.route('/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = resume_service.get_resume_by_id(resume_id)
    
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    return jsonify(resume), 200

@resume_bp.route('/<resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    result = resume_service.delete_resume(resume_id)
    
    if not result:
        return jsonify({'error': 'Resume not found'}), 404
    
    return jsonify({'message': 'Resume deleted successfully'}), 200
