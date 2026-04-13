# AI-Based Resume Screening System

## Project Overview

An intelligent resume screening system that uses AI and machine learning to match candidate educational qualifications with job requirements, streamlining the recruitment process for educational institutions.

## Objectives

1. Design and develop an AI system capable of screening resumes based on education background
2. Integrate machine learning algorithms for accurate matching of educational qualifications with job requirements
3. Assess the effectiveness of the system in improving recruitment processes

## Features

- **AI-Powered Screening**: Automatically analyze resumes and extract educational qualifications
- **Smart Matching**: ML algorithms match candidates with job requirements
- **Dashboard**: Interactive React.js interface for HR teams
- **Analytics**: Performance metrics including accuracy, precision, and recall
- **Resume Upload**: Support for PDF and DOCX resume formats
- **Job Management**: Create and manage job postings with specific educational requirements

## Tech Stack

### Frontend
- React.js
- Axios for API calls
- React Router for navigation
- Modern CSS for styling

### Backend
- Python 3.9+
- Flask for REST API
- scikit-learn for ML algorithms
- spaCy/NLTK for NLP
- PyPDF2 for PDF parsing
- python-docx for DOCX parsing

## Project Structure

```
.
├── frontend/                 # React.js application
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service calls
│   │   └── App.js
│   └── package.json
├── backend/                 # Python Flask application
│   ├── app/
│   │   ├── models/          # ML models and data models
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helper functions
│   ├── requirements.txt
│   └── main.py
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

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Start the backend server:
```bash
python main.py
```

The backend API will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Upload Resumes**: Upload candidate resumes in PDF or DOCX format
2. **Create Job Postings**: Define job requirements with educational qualifications
3. **AI Screening**: The system automatically processes and matches resumes
4. **Review Results**: View ranked candidates based on match scores
5. **Analytics**: Monitor system performance metrics

## ML Model

The system uses:
- **Text Extraction**: Extract text from resume documents
- **NLP Processing**: Parse and identify educational qualifications
- **Feature Engineering**: Create feature vectors from education data
- **Matching Algorithm**: TF-IDF vectorization and cosine similarity
- **Ranking**: Score and rank candidates based on requirements

## API Endpoints

- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes` - Get all resumes
- `POST /api/jobs` - Create job posting
- `GET /api/jobs` - Get all jobs
- `POST /api/match` - Match resumes to job
- `GET /api/analytics` - Get system metrics

## Performance Metrics

- **Accuracy**: Overall correctness of matches
- **Precision**: Ratio of relevant matches to total matches
- **Recall**: Ratio of relevant matches to total relevant candidates
- **F1 Score**: Harmonic mean of precision and recall

## Development

### Running the Full Application

From the root directory:

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

## Research Documentation

This project is part of research on AI-based recruitment systems. Results and methodology will be documented for publication.

## Contributing

This is a research project for EmpowerTech Solutions. For questions or contributions, please contact the development team.

## License

Copyright © 2024 EmpowerTech Solutions. All rights reserved.

## Contact

EmpowerTech Solutions  
Chennai, Tamil Nadu, India
