from flask import Blueprint, request, jsonify

from app.services.job_service import JobService

job_bp = Blueprint('job', __name__)
job_service = JobService()

@job_bp.route('', methods=['POST'])
def create_job():
    data = request.get_json()
    
    required_fields = ['title', 'description', 'requirements']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    result = job_service.create_job(data)
    return jsonify(result), 201

@job_bp.route('', methods=['GET'])
def get_jobs():
    jobs = job_service.get_all_jobs()
    return jsonify(jobs), 200

@job_bp.route('/<job_id>', methods=['GET'])
def get_job(job_id):
    job = job_service.get_job_by_id(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job), 200

@job_bp.route('/<job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    result = job_service.update_job(job_id, data)
    
    if not result:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(result), 200

@job_bp.route('/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    result = job_service.delete_job(job_id)
    
    if not result:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify({'message': 'Job deleted successfully'}), 200
