from flask import Blueprint, request, jsonify
import json
import os
from app.services.evaluation_service import EvaluationService
from app.services.matching_service import MatchingService

evaluation_bp = Blueprint('evaluation', __name__)
evaluation_service = EvaluationService()
matching_service = MatchingService()

@evaluation_bp.route('/run-test', methods=['POST'])
def run_evaluation_test():
    """Run evaluation test using ground truth dataset"""
    try:
        data_path = os.path.join('backend', 'data', 'test_dataset.json')
        if not os.path.exists(data_path):
            data_path = os.path.join('data', 'test_dataset.json')
        
        with open(data_path, 'r') as f:
            test_data = json.load(f)
        
        predictions = []
        threshold = request.json.get('threshold', 0.5) if request.json else 0.5
        
        for test_case in test_data['test_cases']:
            score_result = matching_service.matcher.calculate_match_score(
                test_case['candidate_education'],
                test_case['job_requirements']
            )
            
            predictions.append({
                'resume_id': test_case['resume_id'],
                'job_id': test_case['job_id'],
                'score': score_result,
                'threshold': threshold,
                'test_case_id': test_case['id']
            })
        
        ground_truth = [
            {
                'resume_id': tc['resume_id'],
                'job_id': tc['job_id'],
                'is_match': tc['is_match']
            }
            for tc in test_data['test_cases']
        ]
        
        metrics = evaluation_service.calculate_metrics(predictions, ground_truth)
        distribution = evaluation_service.calculate_score_distribution(predictions)
        
        experiment_name = request.json.get('experiment_name') if request.json else None
        saved_file = evaluation_service.save_evaluation_results({
            'metrics': metrics,
            'distribution': distribution,
            'threshold': threshold,
            'predictions': predictions[:5]
        }, experiment_name)
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'distribution': distribution,
            'saved_to': saved_file,
            'total_test_cases': len(test_data['test_cases'])
        }), 200
        
    except FileNotFoundError:
        return jsonify({
            'error': 'Test dataset not found',
            'path_tried': data_path
        }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@evaluation_bp.route('/metrics', methods=['POST'])
def calculate_custom_metrics():
    """Calculate metrics for custom predictions and ground truth"""
    try:
        data = request.get_json()
        predictions = data.get('predictions', [])
        ground_truth = data.get('ground_truth', [])
        
        if not predictions or not ground_truth:
            return jsonify({'error': 'predictions and ground_truth are required'}), 400
        
        metrics = evaluation_service.calculate_metrics(predictions, ground_truth)
        
        return jsonify(metrics), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@evaluation_bp.route('/results', methods=['GET'])
def get_evaluation_results():
    """Get all saved evaluation results"""
    try:
        results_dir = evaluation_service.results_dir
        
        if not os.path.exists(results_dir):
            return jsonify({'results': []}), 200
        
        results = []
        for filename in os.listdir(results_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(results_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    data['filename'] = filename
                    results.append(data)
        
        results.sort(key=lambda x: x.get('metrics', {}).get('timestamp', ''), reverse=True)
        
        return jsonify({'results': results}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@evaluation_bp.route('/compare', methods=['POST'])
def compare_results():
    """Compare multiple evaluation results"""
    try:
        data = request.get_json()
        result_files = data.get('result_files', [])
        
        if not result_files:
            return jsonify({'error': 'result_files array is required'}), 400
        
        results = []
        for filename in result_files:
            filepath = os.path.join(evaluation_service.results_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    results.append(json.load(f))
        
        comparison = evaluation_service.compare_algorithms(
            [r.get('metrics', r) for r in results]
        )
        
        return jsonify(comparison), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@evaluation_bp.route('/score-distribution', methods=['POST'])
def get_score_distribution():
    """Get distribution of scores for predictions"""
    try:
        data = request.get_json()
        predictions = data.get('predictions', [])
        
        if not predictions:
            return jsonify({'error': 'predictions array is required'}), 400
        
        distribution = evaluation_service.calculate_score_distribution(predictions)
        
        return jsonify(distribution), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
