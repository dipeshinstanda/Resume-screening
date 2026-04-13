# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Resume Endpoints

#### Upload Resume
Upload a resume file for processing.

**Endpoint:** `POST /resumes/upload`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF or DOCX)

**Response:**
```json
{
  "id": "uuid",
  "filename": "resume.pdf",
  "education": [
    {
      "degree": "Bachelor's",
      "field": "Computer Science",
      "institution": "University Name",
      "year": "2023"
    }
  ],
  "message": "Resume processed successfully"
}
```

#### Get All Resumes
Retrieve all uploaded resumes.

**Endpoint:** `GET /resumes`

**Response:**
```json
[
  {
    "id": "uuid",
    "filename": "resume.pdf",
    "education": [...],
    "uploaded_at": "2024-01-01T00:00:00",
    "status": "processed"
  }
]
```

#### Get Resume by ID
Retrieve a specific resume.

**Endpoint:** `GET /resumes/:id`

**Response:**
```json
{
  "id": "uuid",
  "filename": "resume.pdf",
  "text": "Full resume text...",
  "education": [...],
  "uploaded_at": "2024-01-01T00:00:00",
  "status": "processed"
}
```

#### Delete Resume
Delete a resume.

**Endpoint:** `DELETE /resumes/:id`

**Response:**
```json
{
  "message": "Resume deleted successfully"
}
```

### 2. Job Endpoints

#### Create Job
Create a new job posting.

**Endpoint:** `POST /jobs`

**Request:**
```json
{
  "title": "Software Engineer",
  "description": "Job description...",
  "requirements": [
    "2+ years experience",
    "Strong coding skills"
  ],
  "education_requirements": [
    "Bachelor's in Computer Science",
    "Master's preferred"
  ]
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Software Engineer",
  "description": "Job description...",
  "requirements": [...],
  "education_requirements": [...],
  "created_at": "2024-01-01T00:00:00",
  "status": "active"
}
```

#### Get All Jobs
Retrieve all job postings.

**Endpoint:** `GET /jobs`

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Software Engineer",
    ...
  }
]
```

#### Get Job by ID
Retrieve a specific job.

**Endpoint:** `GET /jobs/:id`

#### Update Job
Update a job posting.

**Endpoint:** `PUT /jobs/:id`

#### Delete Job
Delete a job posting.

**Endpoint:** `DELETE /jobs/:id`

### 3. Matching Endpoints

#### Match Resumes to Job
Find matching resumes for a job.

**Endpoint:** `POST /match`

**Request:**
```json
{
  "job_id": "uuid",
  "threshold": 0.5
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "job_title": "Software Engineer",
  "total_matches": 5,
  "matches": [
    {
      "resume_id": "uuid",
      "filename": "resume.pdf",
      "score": 0.85,
      "education": [...]
    }
  ]
}
```

#### Calculate Match Score
Calculate score between a resume and job.

**Endpoint:** `POST /match/score`

**Request:**
```json
{
  "resume_id": "uuid",
  "job_id": "uuid"
}
```

**Response:**
```json
{
  "resume_id": "uuid",
  "job_id": "uuid",
  "score": 0.75
}
```

### 4. Analytics Endpoints

#### Get System Metrics
Get overall system statistics.

**Endpoint:** `GET /analytics`

**Response:**
```json
{
  "total_resumes": 50,
  "total_jobs": 10,
  "processed_resumes": 48,
  "active_jobs": 8
}
```

#### Get Performance Metrics
Get ML model performance metrics.

**Endpoint:** `GET /analytics/performance`

**Response:**
```json
{
  "accuracy": 0.0,
  "precision": 0.0,
  "recall": 0.0,
  "f1_score": 0.0,
  "note": "Performance metrics will be calculated after model training"
}
```

## Error Responses

All endpoints return appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

Error response format:
```json
{
  "error": "Error message"
}
```
