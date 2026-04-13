# Sample Data for Testing

## Sample Resume Text

### Sample 1: Computer Science Graduate
```
John Doe
Email: john.doe@email.com
Phone: +91-9876543210

Education:
Bachelor of Technology in Computer Science
Anna University, Chennai
2019 - 2023

Skills: Python, Java, Machine Learning, Data Structures

Experience:
Intern at Tech Corp (2022-2023)
```

### Sample 2: MBA Graduate
```
Jane Smith
Email: jane.smith@email.com
Phone: +91-9876543211

Education:
Master of Business Administration
Indian Institute of Management, Bangalore
2021 - 2023

Bachelor of Commerce
University of Delhi
2017 - 2020

Skills: Business Analytics, Leadership, Strategic Planning
```

### Sample 3: PhD Candidate
```
Dr. Raj Kumar
Email: raj.kumar@email.com
Phone: +91-9876543212

Education:
PhD in Artificial Intelligence
IIT Madras
2020 - Present

Master of Science in Computer Science
IIT Delhi
2018 - 2020

Bachelor of Engineering in Information Technology
VIT University
2014 - 2018
```

## Sample Job Descriptions

### Job 1: Software Engineer
```
Title: Software Engineer
Description: We are looking for a talented software engineer to join our team.

Requirements:
- 2+ years of experience
- Strong problem-solving skills
- Team player

Education Requirements:
- Bachelor's degree in Computer Science or related field
- Master's degree preferred
```

### Job 2: Business Analyst
```
Title: Business Analyst
Description: Seeking an experienced business analyst for our consulting team.

Requirements:
- 3+ years of experience
- Excellent communication skills
- Analytical mindset

Education Requirements:
- MBA or Master's in Business Administration
- Bachelor's in Business, Commerce, or related field
```

### Job 3: Research Scientist
```
Title: AI Research Scientist
Description: Join our AI research team working on cutting-edge technologies.

Requirements:
- Strong research background
- Published papers preferred
- Deep learning expertise

Education Requirements:
- PhD in Computer Science, AI, or related field
- Master's degree minimum
```

## Test Cases

### Test Case 1: Perfect Match
- Resume: PhD in Computer Science
- Job: PhD required
- Expected Score: > 0.9

### Test Case 2: Over-qualified
- Resume: PhD in Computer Science
- Job: Bachelor's required
- Expected Score: > 0.7

### Test Case 3: Under-qualified
- Resume: Bachelor's in Computer Science
- Job: PhD required
- Expected Score: < 0.6

### Test Case 4: Field Mismatch
- Resume: Bachelor's in Mechanical Engineering
- Job: Bachelor's in Computer Science
- Expected Score: < 0.5

### Test Case 5: Exact Match
- Resume: MBA
- Job: MBA required
- Expected Score: > 0.8
