# 🚀 Resume Checker - Quick Start Guide

## What is Resume Checker?

Resume Checker is a **free tool** that helps you optimize your resume for specific job applications. It analyzes your resume against a job description and shows you:

- **Match Score**: How well your resume aligns with the job (0-100%)
- **Matching Keywords**: Skills and terms you got right ✅
- **Missing Keywords**: Important skills you should add ⚠️
- **Detailed Breakdown**: Scores for different aspects
- **Recommendations**: Actionable tips to improve your resume

## 🎯 How to Use (3 Simple Steps)

### Step 1: Start the Servers

**Option A: Using the launcher script (Windows)**
```bash
# Double-click this file:
RUN_SERVERS.bat

# Or run in PowerShell:
.\RUN_SERVERS.ps1
```

**Option B: Manual start**
```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Step 2: Open Resume Checker
1. Open your browser to: `http://localhost:3000`
2. Click **"Resume Checker"** in the navigation menu
3. You'll see two text areas

### Step 3: Analyze Your Resume
1. **Upload/Paste Resume**:
   - Click "Choose file" to upload PDF/DOCX
   - OR paste your resume text directly

2. **Paste Job Description**:
   - Copy the full job posting
   - Paste into the right text area

3. **Click "✨ Analyze Match"**
   - Results appear in ~1 second

## 📊 Understanding Your Results

### Overall Alignment Score
- **70-100%**: 🟢 Excellent match! Apply with confidence
- **50-69%**: 🟡 Good match, consider adding missing keywords
- **0-49%**: 🔴 Needs improvement, review missing keywords

### Matched Keywords (Green Tags)
These are skills/terms found in both your resume and the JD. Great!

### Missing Keywords (Red Tags)
These appear in the JD but not in your resume. Consider adding them if relevant.

### Breakdown Metrics
- **Keyword Match**: Overall keyword alignment
- **Skills Coverage**: Percentage of required skills you have
- **Completeness**: How comprehensive your resume is

## 💡 Tips for Best Results

### ✅ DO:
- Use the **full job description** (don't truncate)
- Include **all sections** of your resume (experience, skills, education)
- Review **missing keywords** and add relevant ones
- **Re-analyze** after making changes
- Focus on **legitimate skills** you actually have

### ❌ DON'T:
- Don't just stuff keywords without context
- Don't claim skills you don't have
- Don't ignore missing keywords that are critical
- Don't expect 100% match (70%+ is excellent)

## 🎓 Example Workflow

### 1. Initial Analysis
```
Resume Score: 45%
Missing: Docker, Kubernetes, CI/CD, Agile, Python
Recommendation: "Consider adding more relevant keywords"
```

### 2. Update Resume
Add missing skills to relevant sections:
```
Skills:
- Docker & Kubernetes for container orchestration
- CI/CD pipeline development with Jenkins
- Agile/Scrum methodologies
- Python development (3+ years)
```

### 3. Re-analyze
```
Resume Score: 78%
Matched: Docker, Kubernetes, CI/CD, Agile, Python
Recommendation: "Great match! Your resume aligns well"
```

## 🛠️ Testing the Feature

Want to test if it works? Run this:

```bash
# Make sure backend is running first
python test_resume_checker.py
```

You should see:
```
✅ API Call Successful!
Overall Alignment: 75.50%
✅ Test Passed!
```

## 📁 Sample Resumes & Job Descriptions

### Sample Resume
```
Jane Smith
Data Scientist

Skills:
- Python, R, SQL
- Machine Learning (scikit-learn, TensorFlow)
- Data Visualization (Matplotlib, Seaborn)
- Statistics & Probability
- Pandas, NumPy, Jupyter

Experience:
- 4 years as Data Analyst
- Built predictive models for customer churn
- Developed dashboards using Tableau
- Worked with large datasets (10M+ records)

Education:
- MS in Data Science
- BS in Statistics
```

### Sample Job Description
```
Data Scientist - Machine Learning

Requirements:
- 3+ years Python and R experience
- Strong background in Machine Learning
- Experience with scikit-learn or TensorFlow
- Proficiency in Pandas and NumPy
- Data visualization skills
- SQL knowledge
- Master's degree in related field

Nice to have:
- Deep Learning experience
- Cloud platforms (AWS/Azure)
- Spark or Hadoop
```

**Expected Match**: ~80-85%

## 🐛 Troubleshooting

### "Failed to analyze" error
**Solution**: Make sure backend is running
```bash
cd backend
python main.py
```

### "Connection refused" error
**Solution**: Check if backend is on port 5000
```bash
# Should see: "Running on http://0.0.0.0:5000"
```

### Low match score
**Solution**: This is normal! Most resumes score 50-70% initially. Use the recommendations to improve.

### No results appearing
**Solution**: Make sure both text areas have content (not empty)

## 🎨 Features in Action

### Visual Highlights
- **Matched keywords** appear as green tags
- **Missing keywords** appear as red tags
- **Score circle** changes color based on match percentage

### Interactive Elements
- Hover over keywords to see frequency
- Click recommendations for tips
- View detailed breakdown with progress bars

## 📚 More Information

- **Full Documentation**: `docs/RESUME_CHECKER_GUIDE.md`
- **API Reference**: Check the guide for endpoint details
- **Source Code**: 
  - Backend: `backend/app/routes/resume_checker_routes.py`
  - Frontend: `frontend/src/pages/ResumeChecker.js`

## ❓ FAQ

**Q: Is my data stored anywhere?**
A: No, all analysis happens in real-time. Nothing is saved.

**Q: Can I use this for multiple jobs?**
A: Yes! Just paste different job descriptions and re-analyze.

**Q: What file formats are supported?**
A: Currently: PDF, DOCX, and plain text.

**Q: Will this guarantee me a job?**
A: No, but it helps optimize your resume for ATS systems and recruiters.

**Q: Is this free?**
A: Yes, completely free and open-source!

## 🎉 Ready to Go!

1. Start servers: `.\RUN_SERVERS.bat`
2. Open: `http://localhost:3000/resume-checker`
3. Upload resume + paste job description
4. Click "Analyze Match"
5. Get instant feedback!

---

**Good luck with your job applications! 🚀**
