import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Testing AI Resume Screening System components...")
print("-" * 50)

# Test 1: Import ML Model
try:
    from app.models.ml_model import EducationMatcher
    print("✓ ML Model imported successfully")
    matcher = EducationMatcher()
    print("✓ EducationMatcher instantiated")
except Exception as e:
    print(f"✗ ML Model import failed: {e}")
    sys.exit(1)

# Test 2: Import Services
try:
    from app.services.resume_service import ResumeService
    from app.services.job_service import JobService
    from app.services.matching_service import MatchingService
    from app.services.analytics_service import AnalyticsService
    print("✓ All services imported successfully")
except Exception as e:
    print(f"✗ Services import failed: {e}")
    sys.exit(1)

# Test 3: Import Utilities
try:
    from app.utils.pdf_parser import extract_text_from_pdf
    from app.utils.docx_parser import extract_text_from_docx
    from app.utils.education_extractor import extract_education
    print("✓ All utilities imported successfully")
except Exception as e:
    print(f"✗ Utilities import failed: {e}")
    sys.exit(1)

# Test 4: Test Education Extraction
try:
    sample_text = """
    John Doe
    Education:
    Bachelor of Science in Computer Science
    MIT, 2020
    """
    education = extract_education(sample_text)
    print(f"✓ Education extraction works: {len(education)} degree(s) found")
except Exception as e:
    print(f"✗ Education extraction failed: {e}")
    sys.exit(1)

# Test 5: Test Matching Algorithm
try:
    candidate_edu = [{'degree': 'Bachelor', 'field': 'Computer Science', 'institution': 'MIT', 'year': '2020'}]
    job_req = ['Bachelor degree in Computer Science']
    score = matcher.calculate_match_score(candidate_edu, job_req)
    print(f"✓ Matching algorithm works: Score = {score}")
except Exception as e:
    print(f"✗ Matching algorithm failed: {e}")
    sys.exit(1)

# Test 6: Import Flask App
try:
    import main
    print("✓ Flask app imported successfully")
except Exception as e:
    print(f"✗ Flask app import failed: {e}")
    sys.exit(1)

print("-" * 50)
print("All tests passed! ✓")
print("\nBackend is ready to run.")
print("Start the server with: py backend/main.py")
