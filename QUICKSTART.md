# Quick Start Guide

## AI-Based Resume Screening System
**EmpowerTech Solutions, Chennai**

### Step 1: Install Python Dependencies

Open a terminal in the backend directory:

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

Open a terminal in the frontend directory:

```bash
cd frontend
npm install
```

### Step 3: Start the Backend Server

In the backend directory:

```bash
python main.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 4: Start the Frontend

In a new terminal, in the frontend directory:

```bash
npm start
```

The application will open in your browser at `http://localhost:3000`

### Step 5: Using the Application

1. **Dashboard** - View system statistics
2. **Upload Resume** - Upload PDF or DOCX resumes
3. **Jobs** - Create job postings with educational requirements
4. **Match Results** - Find matching candidates for jobs
5. **Analytics** - View performance metrics

## Testing the System

### Test Resume Upload

1. Go to "Upload Resume"
2. Select a PDF or DOCX resume file
3. Click "Upload Resume"
4. View the extracted education information

### Test Job Creation

1. Go to "Jobs"
2. Click "Create New Job"
3. Fill in:
   - Job Title: "Software Engineer"
   - Description: "Looking for a software engineer"
   - Requirements: "2+ years experience" (one per line)
   - Education: "Bachelor's in Computer Science" (one per line)
4. Click "Create Job"

### Test Matching

1. Go to "Match Results"
2. Select a job from the dropdown
3. Adjust the threshold (0.0 to 1.0)
4. Click "Find Matches"
5. View ranked candidates

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -i :5000
kill -9 <process_id>
```

**Module not found:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

### Frontend Issues

**Port 3000 in use:**
- The app will ask if you want to use a different port
- Choose 'Y' to use port 3001

**npm install fails:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Upload sample resumes
- Create job postings
- Test the matching algorithm
- Review the analytics
- Customize the UI
- Add more features

## Support

For issues or questions, refer to:
- [README.md](../README.md)
- [API Documentation](../docs/API_DOCUMENTATION.md)
- [Research Notes](../docs/RESEARCH.md)

---

