"""
Test script for Resume Checker API
"""
import requests
import json
import os

BASE_URL = "http://localhost:5000"

def test_text_extraction():
    """Test the text extraction endpoint"""
    print("Testing Text Extraction Endpoint...")
    print("=" * 50)

    # Check if sample file exists
    sample_file = "sample_resume.txt"
    if not os.path.exists(sample_file):
        # Create a sample file
        with open(sample_file, 'w') as f:
            f.write("""
            John Doe
            Software Engineer

            Skills: Python, JavaScript, React, Flask, Docker, Kubernetes
            Experience: 3 years Backend Developer
            Education: BS Computer Science
            """)
        print(f"Created sample file: {sample_file}")

    try:
        with open(sample_file, 'rb') as f:
            response = requests.post(
                f"{BASE_URL}/api/resume-checker/extract-text",
                files={'file': f}
            )

        if response.status_code == 200:
            data = response.json()
            print("✅ Text Extraction Successful!")
            print(f"Filename: {data['filename']}")
            print(f"Extracted text length: {len(data['text'])} characters")
            print()
            return data['text']
        else:
            print(f"❌ Text Extraction Failed: {response.status_code}")
            print(response.json())
            return None

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_resume_checker():
    """Test the resume checker endpoint"""

    # Sample resume text
    resume_text = """
    John Doe
    Software Engineer
    
    Skills:
    - Python, JavaScript, React
    - Machine Learning, Data Science
    - Flask, Django, FastAPI
    - Docker, Kubernetes
    - Git, CI/CD
    
    Experience:
    - 3 years as Backend Developer
    - Built REST APIs with Flask
    - Developed ML models with scikit-learn
    - Worked with React.js frontend
    
    Education:
    - BS in Computer Science
    - MS in Artificial Intelligence
    """
    
    # Sample job description
    jd_text = """
    Senior Software Engineer - AI/ML Focus
    
    Requirements:
    - 3+ years of Python development
    - Experience with Machine Learning and scikit-learn
    - Strong background in React.js
    - Knowledge of Flask or Django
    - Docker and Kubernetes experience
    - Understanding of CI/CD pipelines
    - Bachelor's degree in Computer Science
    
    Nice to have:
    - Experience with TensorFlow or PyTorch
    - Cloud platforms (AWS, Azure, GCP)
    - Agile methodology
    """
    
    # Make API call
    print("Testing Resume Checker API...")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/resume-checker/analyze",
            json={
                "resume_text": resume_text,
                "jd_text": jd_text
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ API Call Successful!")
            print()
            
            print("📊 ANALYSIS RESULTS:")
            print("=" * 50)
            
            # Overall score
            breakdown = data['breakdown']
            print(f"Overall Alignment: {breakdown['overall_alignment']:.2f}%")
            print(f"Keyword Match: {breakdown['keyword_match']:.2f}%")
            print(f"Skills Coverage: {breakdown['skills_coverage']:.2f}%")
            print(f"Completeness: {breakdown['completeness']:.2f}%")
            print()

            # Match details
            analysis = data['analysis']
            print(f"Total Keywords in JD: {analysis['total_keywords_in_jd']}")
            print(f"Matched Keywords: {analysis['matched_keywords_count']}")
            print(f"Missing Keywords: {analysis['missing_keywords_count']}")
            print()

            # Top matched keywords
            print("✅ Top Matched Keywords:")
            for item in analysis['matched_keywords'][:10]:
                print(f"  - {item['keyword']} (appears {item['resume_count']}x in resume)")
            print()

            # Missing keywords
            if analysis['missing_keywords']:
                print("⚠️ Top Missing Keywords:")
                for item in analysis['missing_keywords'][:5]:
                    print(f"  - {item['keyword']} (appears {item['jd_count']}x in JD)")
                print()

            # Recommendations
            if data['recommendations']:
                print("💡 Recommendations:")
                for rec in data['recommendations']:
                    print(f"  - {rec}")
                print()

            print("=" * 50)
            print("✅ Test Passed!")

        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.json())

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running")
        print("   Run: python backend/main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Testing Resume Checker API")
    print("=" * 50)
    print()

    # Test 1: Text extraction
    print("TEST 1: Text Extraction")
    extracted_text = test_text_extraction()
    print()

    # Test 2: Resume analysis
    print("TEST 2: Resume Analysis")
    test_resume_checker()

