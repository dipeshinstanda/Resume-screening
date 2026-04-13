from flask import Blueprint, jsonify

from app.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)
analytics_service = AnalyticsService()

@analytics_bp.route('', methods=['GET'])
def get_analytics():
    metrics = analytics_service.get_system_metrics()
    return jsonify(metrics), 200

@analytics_bp.route('/performance', methods=['GET'])
def get_performance():
    performance = analytics_service.get_performance_metrics()
    return jsonify(performance), 200
