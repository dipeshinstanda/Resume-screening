# AI-Based Resume Screening System


## Overview

An intelligent resume screening system that uses AI and machine learning to match candidate educational qualifications with job requirements, streamlining the recruitment process for educational institutions.

## Objectives

1. To design and develop an AI system capable of screening resumes based on the education background of candidates
2. To integrate machine learning algorithms for accurate matching of educational qualifications with job requirements
3. To assess the effectiveness of the system in improving recruitment processes for educational institutions

## Tasks

1. Research and gather data on existing AI technologies used in resume screening
2. Develop algorithms for the AI system to analyze and match education qualifications with job requirements
3. Collect and process a dataset of resumes and job descriptions for training and testing the AI system
4. Evaluate the performance of the system through accuracy, precision, and recall metrics
5. Document the process and results of the project in a formal research paper for publication

## Features

- **🎯 Resume Checker**: Upload your resume and compare it with a job description to see match score, matching keywords, and gaps *(NEW!)*
- **AI-Powered Screening**: Automatically analyze resumes and extract educational qualifications
- **Smart Matching**: ML algorithms match candidates with job requirements
- **React.js Dashboard**: Interactive web interface for HR teams
- **Analytics**: Performance metrics including accuracy, precision, and recall
- **Resume Upload**: Support for PDF and DOCX resume formats
- **Job Management**: Create and manage job postings with specific educational requirements
- **Visual Keyword Highlighting**: See exactly which keywords match and which are missing *(NEW!)*
- **Detailed Breakdown**: Get scores for keyword match, skills coverage, and completeness *(NEW!)*

## Tech Stack

### Frontend
- React.js with React Router
- Axios for API calls
- Modern CSS styling

### Backend
- Python 3.9+ with Flask
- scikit-learn for ML algorithms
- PyPDF2 and python-docx for document parsing
- NLP for text processing

## Project Structure

```
.
├── frontend/                 # React.js application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── App.js
│   └── package.json
├── backend/                 # Python Flask API
│   ├── app/
│   │   ├── models/          # ML models
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utilities
│   ├── requirements.txt
│   └── main.py
├── docs/                    # Documentation
├── .github/
│   └── copilot-instructions.md
└── README.md
```

## Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+
- pip

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file (optional):
```bash
cp .env.example .env
```

4. Start the backend server:
```bash
python main.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend runs on `http://localhost:3000`

## Usage

1. **Upload Resumes**: Navigate to "Upload Resume" and upload PDF or DOCX files
2. **Create Jobs**: Go to "Jobs" to create job postings with educational requirements
3. **Match Candidates**: Use "Match Results" to find suitable candidates for jobs
4. **View Analytics**: Check "Analytics" for system performance metrics

## Running the Application

### Option 1: Manual Start
```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Option 2: Using VS Code Tasks
Press `Ctrl+Shift+P` > `Tasks: Run Task` > `Start Full Application`

## ML Algorithm

The system uses:
- **Text Extraction**: PyPDF2 and python-docx for document parsing
- **Education Extraction**: Regex patterns to identify degrees, fields, and institutions
- **TF-IDF Vectorization**: Convert text to numerical features
- **Cosine Similarity**: Measure similarity between resume and job requirements
- **Degree Hierarchy**: Rank candidates based on education level
- **Scoring**: Combined score (60% similarity + 40% degree match)

## API Endpoints

- `POST /api/resumes/upload` - Upload and process resume
- `GET /api/resumes` - Get all resumes
- `POST /api/jobs` - Create job posting
- `GET /api/jobs` - Get all jobs
- `POST /api/match` - Match resumes to job
- `GET /api/analytics` - Get system metrics

See [API Documentation](docs/API_DOCUMENTATION.md) for details.

## Performance Metrics

The system evaluates matching accuracy using:
- **Accuracy**: Overall correctness
- **Precision**: Relevant matches / Total matches
- **Recall**: Relevant matches / Total relevant
- **F1 Score**: Harmonic mean of precision and recall

## Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Research Notes](docs/RESEARCH.md)
- [Sample Data](docs/SAMPLE_DATA.md)

## Research

This project is part of research on AI-based recruitment systems by EmpowerTech Solutions. Results will be documented for publication.

## License

Copyright © 2024 EmpowerTech Solutions. All rights reserved.

## Contact

