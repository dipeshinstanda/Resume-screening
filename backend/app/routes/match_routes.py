from flask import Blueprint, request, jsonify

from app.services.matching_service import MatchingService

match_bp = Blueprint('match', __name__)
matching_service = MatchingService()

@match_bp.route('', methods=['POST'])
def match_resumes():
    data = request.get_json()
    
    if 'job_id' not in data:
        return jsonify({'error': 'job_id is required'}), 400
    
    job_id = data['job_id']
    threshold = data.get('threshold', 0.5)
    
    results = matching_service.match_resumes_to_job(job_id, threshold)
    
    if 'error' in results:
        return jsonify(results), 404
    
    return jsonify(results), 200

@match_bp.route('/score', methods=['POST'])
def calculate_score():
    data = request.get_json()
    
    if 'resume_id' not in data or 'job_id' not in data:
        return jsonify({'error': 'resume_id and job_id are required'}), 400
    
    result = matching_service.calculate_match_score(data['resume_id'], data['job_id'])
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify(result), 200
