# Developer Guide

## AI-Based Resume Screening System
**EmpowerTech Solutions**

This guide provides detailed information for developers working on the AI Resume Screening System.

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React.js)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Dashboard  │  │ Upload Resume│  │     Jobs     │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
│  ┌─────────────┐  ┌──────────────┐                     │
│  │   Matching  │  │  Analytics   │                     │
│  └─────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                          │
                    HTTP/REST API
                          │
┌─────────────────────────────────────────────────────────┐
│                    Backend (Flask)                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │              API Routes Layer                     │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐        │  │
│  │  │Resume│ │ Jobs │ │Match │ │Analytics │        │  │
│  │  └──────┘ └──────┘ └──────┘ └──────────┘        │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Services Layer                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │  │
│  │  │ Resume   │ │   Job    │ │ Matching │         │  │
│  │  │ Service  │ │ Service  │ │ Service  │         │  │
│  │  └──────────┘ └──────────┘ └──────────┘         │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │              ML/NLP Layer                         │  │
│  │  ┌─────────────┐ ┌──────────────┐               │  │
│  │  │  Education  │ │   Matching   │               │  │
│  │  │  Extractor  │ │   Algorithm  │               │  │
│  │  └─────────────┘ └──────────────┘               │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Utils Layer                          │  │
│  │  ┌──────────┐ ┌──────────┐                       │  │
│  │  │   PDF    │ │  DOCX    │                       │  │
│  │  │  Parser  │ │  Parser  │                       │  │
│  │  └──────────┘ └──────────┘                       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Backend Development

### Project Structure

```
backend/
├── app/
│   ├── models/          # ML models and algorithms
│   ├── routes/          # API endpoint definitions
│   ├── services/        # Business logic
│   └── utils/           # Helper functions
├── uploads/             # Uploaded resume files
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

### Adding a New API Endpoint

1. **Create a route file** in `app/routes/`:

```python
# app/routes/new_feature_routes.py
from flask import Blueprint, request, jsonify
from app.services.new_feature_service import NewFeatureService

new_feature_bp = Blueprint('new_feature', __name__)
new_feature_service = NewFeatureService()

@new_feature_bp.route('', methods=['GET'])
def get_data():
    data = new_feature_service.get_data()
    return jsonify(data), 200
```

2. **Create a service** in `app/services/`:

```python
# app/services/new_feature_service.py
class NewFeatureService:
    def __init__(self):
        # Initialize service
        pass
    
    def get_data(self):
        # Business logic here
        return {"message": "Success"}
```

3. **Register the blueprint** in `main.py`:

```python
from app.routes.new_feature_routes import new_feature_bp

app.register_blueprint(new_feature_bp, url_prefix='/api/new-feature')
```

### ML Model Development

The matching algorithm is in `app/models/ml_model.py`:

```python
class EducationMatcher:
    def calculate_match_score(self, candidate_education, job_requirements):
        # 1. Text preprocessing
        # 2. TF-IDF vectorization
        # 3. Cosine similarity
        # 4. Degree matching
        # 5. Combined score
        pass
```

**To improve the algorithm:**

1. Add more sophisticated NLP:
```python
import spacy
nlp = spacy.load('en_core_web_sm')
```

2. Use deep learning models:
```python
from transformers import BertTokenizer, BertModel
```

3. Add skill matching:
```python
def extract_skills(text):
    # Extract skills from resume
    pass
```

### Testing the Backend

```bash
# Test a specific endpoint
curl http://localhost:5000/api/resumes

# Test with sample data
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Job","description":"Test","requirements":[],"education_requirements":[]}'
```

---

## Frontend Development

### Project Structure

```
frontend/src/
├── components/         # Reusable components
│   ├── Header.js
│   └── Header.css
├── pages/             # Page components
│   ├── Dashboard.js
│   ├── UploadResume.js
│   ├── JobManagement.js
│   ├── MatchResults.js
│   └── Analytics.js
├── services/          # API services
│   └── api.js
├── App.js            # Main component
└── App.css           # Global styles
```

### Adding a New Page

1. **Create the page component**:

```javascript
// src/pages/NewFeature.js
import React, { useState, useEffect } from 'react';

function NewFeature() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Load data
  }, []);

  return (
    <div>
      <h2>New Feature</h2>
      {/* Your UI here */}
    </div>
  );
}

export default NewFeature;
```

2. **Add API service** in `src/services/api.js`:

```javascript
export const newFeatureService = {
  getData: async () => {
    const response = await apiClient.get('/new-feature');
    return response.data;
  },
};
```

3. **Add route** in `App.js`:

```javascript
import NewFeature from './pages/NewFeature';

<Route path="/new-feature" element={<NewFeature />} />
```

4. **Add navigation** in `Header.js`:

```javascript
<Link to="/new-feature">New Feature</Link>
```

### Styling Guidelines

- Use the existing CSS classes in `App.css`
- Follow the color scheme:
  - Primary: `#0066cc`
  - Success: `#d4edda`
  - Error: `#f8d7da`
  - Background: `#f5f5f5`

---

## ML/NLP Enhancements

### Current Implementation

1. **Text Extraction**: PyPDF2 and python-docx
2. **Pattern Matching**: Regex for degrees
3. **Vectorization**: TF-IDF
4. **Similarity**: Cosine similarity

### Recommended Improvements

#### 1. Use spaCy for Better NLP

```python
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_education_spacy(text):
    doc = nlp(text)
    education = []
    
    for ent in doc.ents:
        if ent.label_ == 'ORG':  # Organizations (universities)
            education.append({
                'institution': ent.text
            })
    
    return education
```

#### 2. Use BERT for Semantic Matching

```python
from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)
```

#### 3. Add Named Entity Recognition

```python
def extract_entities(text):
    doc = nlp(text)
    return {
        'degrees': [ent.text for ent in doc.ents if ent.label_ == 'DEGREE'],
        'organizations': [ent.text for ent in doc.ents if ent.label_ == 'ORG'],
        'dates': [ent.text for ent in doc.ents if ent.label_ == 'DATE']
    }
```

---

## Database Integration

### Current State
- In-memory storage (dictionaries)
- Data lost on restart

### Recommended: MongoDB

1. **Install MongoDB**:
```bash
pip install pymongo
```

2. **Update services**:

```python
from pymongo import MongoClient

class ResumeService:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client['resume_screening']
        self.resumes = self.db['resumes']
    
    def save_resume(self, resume_data):
        return self.resumes.insert_one(resume_data)
    
    def get_all_resumes(self):
        return list(self.resumes.find())
```

---

## Testing

### Backend Tests

Create `backend/tests/test_resume_service.py`:

```python
import pytest
from app.services.resume_service import ResumeService

def test_process_resume():
    service = ResumeService()
    # Test resume processing
    pass
```

Run tests:
```bash
cd backend
pytest
```

### Frontend Tests

```javascript
// src/pages/Dashboard.test.js
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

test('renders dashboard', () => {
  render(<Dashboard />);
  const heading = screen.getByText(/Dashboard/i);
  expect(heading).toBeInTheDocument();
});
```

Run tests:
```bash
cd frontend
npm test
```

---

## Performance Optimization

### Backend

1. **Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(param):
    # Cached result
    pass
```

2. **Async Processing**:
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def process_resume_async(file_path):
    # Long-running task
    pass
```

### Frontend

1. **React.memo for components**:
```javascript
export default React.memo(MyComponent);
```

2. **Lazy loading**:
```javascript
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
```

---

## Deployment

### Backend (Flask)

**Using Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 main:app
```

**Using Docker**:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Frontend (React)

**Build for production**:
```bash
cd frontend
npm run build
```

**Serve with nginx**:
```nginx
server {
    listen 80;
    location / {
        root /path/to/build;
        try_files $uri /index.html;
    }
    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

---

## Best Practices

### Code Style

**Python (PEP 8)**:
- 4 spaces for indentation
- Max line length: 79 characters
- Use type hints

**JavaScript (Airbnb Style)**:
- 2 spaces for indentation
- Use const/let, avoid var
- Use arrow functions

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push and create PR
git push origin feature/new-feature
```

### Error Handling

**Backend**:
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500
```

**Frontend**:
```javascript
try {
  const data = await api.call();
  setData(data);
} catch (error) {
  setError(error.message);
}
```

---

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- React Documentation: https://react.dev/
- scikit-learn: https://scikit-learn.org/
- spaCy: https://spacy.io/

---

