from flask import Blueprint, request, jsonify
import re
from collections import Counter
from app.utils.text_extractor import extract_text_from_file

resume_checker_bp = Blueprint('resume_checker', __name__)

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    # Convert to lowercase and split into words
    text = text.lower()
    # Remove special characters and split
    words = re.findall(r'\b[a-z]{3,}\b', text)
    
    # Common stop words to exclude
    stop_words = {
        'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'has',
        'will', 'are', 'was', 'were', 'been', 'being', 'can', 'could', 'would',
        'should', 'may', 'might', 'must', 'shall', 'our', 'your', 'their',
        'about', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'again', 'further', 'then', 'once'
    }
    
    # Filter out stop words
    keywords = [word for word in words if word not in stop_words]
    
    return keywords

def find_keyword_positions(text, keyword):
    """Find all positions where a keyword appears in text"""
    positions = []
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    start = 0
    while True:
        pos = text_lower.find(keyword_lower, start)
        if pos == -1:
            break
        positions.append({
            'start': pos,
            'end': pos + len(keyword),
            'context': text[max(0, pos-30):min(len(text), pos+len(keyword)+30)]
        })
        start = pos + 1
    
    return positions

def calculate_skill_match(resume_text, jd_text):
    """Calculate detailed skill matching between resume and JD"""
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    
    # Count keyword frequencies
    resume_freq = Counter(resume_keywords)
    jd_freq = Counter(jd_keywords)
    
    # Find matching keywords
    matching_keywords = set(resume_keywords) & set(jd_keywords)
    
    # Find missing keywords from JD
    missing_keywords = set(jd_keywords) - set(resume_keywords)
    
    # Calculate match percentage
    if len(jd_keywords) > 0:
        match_percentage = (len(matching_keywords) / len(set(jd_keywords))) * 100
    else:
        match_percentage = 0
    
    # Build detailed match data
    matched_words = []
    for keyword in matching_keywords:
        matched_words.append({
            'keyword': keyword,
            'resume_count': resume_freq[keyword],
            'jd_count': jd_freq[keyword],
            'positions_in_resume': find_keyword_positions(resume_text, keyword),
            'positions_in_jd': find_keyword_positions(jd_text, keyword)
        })
    
    # Sort by frequency in JD
    matched_words.sort(key=lambda x: x['jd_count'], reverse=True)
    
    # Build missing keywords data
    missing_words = []
    for keyword in missing_keywords:
        if jd_freq[keyword] > 1:  # Only show keywords mentioned more than once
            missing_words.append({
                'keyword': keyword,
                'jd_count': jd_freq[keyword],
                'positions_in_jd': find_keyword_positions(jd_text, keyword)
            })
    
    # Sort by frequency in JD
    missing_words.sort(key=lambda x: x['jd_count'], reverse=True)
    
    return {
        'match_percentage': round(match_percentage, 2),
        'total_keywords_in_jd': len(set(jd_keywords)),
        'matched_keywords_count': len(matching_keywords),
        'missing_keywords_count': len(missing_keywords),
        'matched_keywords': matched_words[:20],  # Top 20 matches
        'missing_keywords': missing_words[:10]   # Top 10 missing
    }

@resume_checker_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume against job description"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '')
        jd_text = data.get('jd_text', '')
        
        if not resume_text or not jd_text:
            return jsonify({'error': 'Both resume_text and jd_text are required'}), 400
        
        # Calculate detailed matching
        result = calculate_skill_match(resume_text, jd_text)
        
        # Calculate breakdown scores
        breakdown = {
            'overall_alignment': result['match_percentage'],
            'keyword_match': result['match_percentage'],
            'skills_coverage': (result['matched_keywords_count'] / max(result['total_keywords_in_jd'], 1)) * 100,
            'completeness': ((result['total_keywords_in_jd'] - result['missing_keywords_count']) / max(result['total_keywords_in_jd'], 1)) * 100
        }
        
        # Generate recommendations
        recommendations = []
        if result['match_percentage'] < 50:
            recommendations.append("Consider adding more relevant keywords from the job description")
        if result['missing_keywords_count'] > 10:
            recommendations.append(f"You're missing {result['missing_keywords_count']} important keywords")
        if result['match_percentage'] >= 70:
            recommendations.append("Great match! Your resume aligns well with the job description")
        
        return jsonify({
            'success': True,
            'analysis': result,
            'breakdown': breakdown,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_checker_bp.route('/highlight', methods=['POST'])
def get_highlights():
    """Get highlighted text for resume and JD"""
    try:
        data = request.get_json()
        
        resume_text = data.get('resume_text', '')
        jd_text = data.get('jd_text', '')
        
        if not resume_text or not jd_text:
            return jsonify({'error': 'Both texts are required'}), 400

        result = calculate_skill_match(resume_text, jd_text)

        # Create highlight data
        all_keywords = [item['keyword'] for item in result['matched_keywords']]

        return jsonify({
            'success': True,
            'keywords_to_highlight': all_keywords
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_checker_bp.route('/extract-text', methods=['POST'])
def extract_text():
    """Extract text from uploaded resume file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Extract text from file
        text = extract_text_from_file(file)

        if text:
            return jsonify({
                'success': True,
                'text': text,
                'filename': file.filename
            }), 200
        else:
            return jsonify({
                'error': 'Failed to extract text from file. Supported formats: PDF, DOCX, TXT'
            }), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

