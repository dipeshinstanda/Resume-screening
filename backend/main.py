from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.routes.resume_routes import resume_bp
from app.routes.job_routes import job_bp
from app.routes.match_routes import match_bp
from app.routes.analytics_routes import analytics_bp
from app.routes.evaluation_routes import evaluation_bp
from app.routes.resume_checker_routes import resume_checker_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(resume_bp, url_prefix='/api/resumes')
app.register_blueprint(job_bp, url_prefix='/api/jobs')
app.register_blueprint(match_bp, url_prefix='/api/match')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(evaluation_bp, url_prefix='/api/evaluation')
app.register_blueprint(resume_checker_bp, url_prefix='/api/resume-checker')

@app.route('/')
def home():
    return jsonify({
        'message': 'AI Resume Screening System API',
        'company': 'EmpowerTech Solutions',
        'location': 'Chennai, Tamil Nadu, India',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
