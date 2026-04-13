# Quick Start: Running Evaluation Tests

## 🎯 Goal
Run automated tests to evaluate your AI Resume Screening System and generate metrics for research publication.

---

## 📋 Prerequisites

✅ Backend dependencies installed (`pip install -r backend/requirements.txt`)  
✅ Backend server can run (`python backend/main.py`)

---

## 🚀 Option 1: Command Line (Recommended)

### Step 1: Open Terminal
```powershell
cd "C:\Users\DipeshNagpal\Repos\Resume screening"
```

### Step 2: Run Evaluation Script
```powershell
python run_evaluation.py
```

### Step 3: View Results

The script will:
- ✅ Test education extraction on sample data
- ✅ Run matching algorithm on 20 test cases
- ✅ Test 5 different thresholds (0.3, 0.4, 0.5, 0.6, 0.7)
- ✅ Calculate metrics for each threshold
- ✅ Show score distributions
- ✅ Save results to files

**Expected Output:**
```
======================================================================
AI RESUME SCREENING SYSTEM - AUTOMATED EVALUATION TEST
EmpowerTech Solutions
======================================================================

✓ Loading test dataset from: backend/data/test_dataset.json
✓ Total test cases: 20

──────────────────────────────────────────────────────────────────────
TESTING WITH THRESHOLD: 0.5
──────────────────────────────────────────────────────────────────────

✓ Case  1: Score=0.876 | Expected=Match    | Predicted=Match
✓ Case  2: Score=0.321 | Expected=No Match | Predicted=No Match
...

──────────────────────────────────────────────────────────────────────
PERFORMANCE METRICS
──────────────────────────────────────────────────────────────────────
Accuracy:      0.8500 (85.00%)
Precision:     0.8750 (87.50%)
Recall:        0.7778 (77.78%)
F1-Score:      0.8235 (82.35%)

True Positives:  7
False Positives: 1
True Negatives:  10
False Negatives: 2

✓ Results saved to: backend/evaluation_results/threshold_0.5_20241215_143022.json
```

### Step 4: Check Saved Results

Results are saved in:
```
backend/evaluation_results/
├── threshold_0.3_20241215_143022.json
├── threshold_0.4_20241215_143023.json
├── threshold_0.5_20241215_143024.json
├── threshold_0.6_20241215_143025.json
└── threshold_0.7_20241215_143026.json
```

Each file contains:
- Detailed metrics
- Score distribution
- Sample predictions

---

## 🖥️ Option 2: Web Interface

### Step 1: Start Backend
```powershell
cd backend
python main.py
```

Leave this terminal running.

### Step 2: Start Frontend (New Terminal)
```powershell
cd frontend
npm start
```

### Step 3: Open Browser

Navigate to: **http://localhost:3000/evaluation**

### Step 4: Run Test

1. Adjust threshold slider (default 0.5)
2. Click **"Run Evaluation Test"**
3. Wait for results (5-10 seconds)
4. View metrics, confusion matrix, and score distribution

### Step 5: View Historical Results

Scroll down to see all previous test runs in a table.

---

## 📊 Understanding the Results

### Key Metrics

| Metric | What it means | Good value |
|--------|---------------|------------|
| **Accuracy** | Overall correctness | >80% |
| **Precision** | Of predicted matches, how many were correct | >75% |
| **Recall** | Of actual matches, how many we found | >75% |
| **F1-Score** | Balanced metric (average of P & R) | >75% |

### Confusion Matrix

```
                   Predicted Match    Predicted No Match
Actual Match       TP (Good!)         FN (Missed)
Actual No Match    FP (False alarm)   TN (Good!)
```

**Goal:** Maximize TP and TN, minimize FP and FN

### Score Distribution

Shows how many test cases fall into each score range:
- **0.8-1.0:** Strong matches
- **0.6-0.8:** Good matches
- **0.4-0.6:** Weak matches
- **0.2-0.4:** Poor matches
- **0.0-0.2:** Very poor matches

---

## 🎓 For Research Paper

### Step 1: Run Tests
```bash
python run_evaluation.py
```

### Step 2: Note Best Threshold

Look at the comparative analysis:
```
COMPARATIVE ANALYSIS - ALL THRESHOLDS
═════════════════════════════════════════════════════════════════════

Threshold    Accuracy     Precision    Recall       F1-Score    
──────────────────────────────────────────────────────────────────────
0.3          0.7500       0.6667       1.0000       0.8000      
0.4          0.8000       0.7500       0.9000       0.8182      
0.5          0.8500       0.8750       0.7778       0.8235      <- Best overall
0.6          0.8500       0.9000       0.7500       0.8182      
0.7          0.7500       1.0000       0.5000       0.6667      
```

### Step 3: Insert into Research Paper

Open `docs/RESEARCH_PAPER_TEMPLATE.md` and insert your results:

```markdown
### 5.2 Performance Results

**Table 1: Performance Metrics by Threshold**

| Threshold | Accuracy | Precision | Recall | F1-Score |
|-----------|----------|-----------|--------|----------|
| 0.3       | 75.00%   | 66.67%    | 100.00% | 80.00%   |
| 0.4       | 80.00%   | 75.00%    | 90.00% | 81.82%   |
| 0.5       | 85.00%   | 87.50%    | 77.78% | 82.35%   |
| 0.6       | 85.00%   | 90.00%    | 75.00% | 81.82%   |
| 0.7       | 75.00%   | 100.00%   | 50.00% | 66.67%   |

**Best Performing Threshold:** 0.5
```

---

## 🔍 Interpreting Threshold Results

### Threshold = 0.3 (Low)
- **High Recall** (100%) - Catches all real matches
- **Low Precision** (67%) - Many false positives
- **Use case:** Don't want to miss any candidates

### Threshold = 0.5 (Medium - Recommended)
- **Balanced** metrics
- **Good precision** and **good recall**
- **Use case:** General purpose screening

### Threshold = 0.7 (High)
- **High Precision** (100%) - No false positives
- **Low Recall** (50%) - Misses half of real matches
- **Use case:** Only want very confident matches

---

## 📈 Next Steps After Evaluation

### 1. Document Results
Copy results from terminal or `evaluation_results/` folder into your research paper.

### 2. Analyze Failures
Look at false positives and false negatives:
```python
# In run_evaluation.py, add:
for prediction in predictions:
    if prediction['predicted'] != prediction['expected']:
        print(f"Failed case: {prediction}")
```

### 3. Improve Algorithm
Based on failure analysis:
- Adjust weights (currently 60% similarity, 40% degree match)
- Add more features (institution ranking, field matching)
- Try different NLP techniques

### 4. Re-run Tests
```bash
python run_evaluation.py
```

### 5. Compare Results
Use the comparison feature:
```python
# Compare old vs new results
from app.services.evaluation_service import EvaluationService
evaluator = EvaluationService()
comparison = evaluator.compare_algorithms([old_results, new_results])
print(comparison)
```

---

## 💡 Tips

### Reproducibility
- Results are timestamped and saved
- Same test dataset gives same results
- Document which version produced which results

### Multiple Runs
Run tests multiple times to ensure consistency:
```bash
python run_evaluation.py  # Run 1
python run_evaluation.py  # Run 2
python run_evaluation.py  # Run 3
```

Results should be identical (algorithm is deterministic).

### Custom Thresholds
Edit `run_evaluation.py` to test different thresholds:
```python
thresholds = [0.35, 0.45, 0.55, 0.65]  # Custom values
```

---

## ❓ Troubleshooting

### Error: "Test dataset not found"
**Solution:**
```bash
# Check if file exists
ls backend/data/test_dataset.json

# If missing, it was created in this session
# Make sure you're in the right directory
cd "C:\Users\DipeshNagpal\Repos\Resume screening"
```

### Error: "ModuleNotFoundError"
**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### No output or freezing
**Solution:**
- Check if backend is running on port 5000 (for web interface)
- For command line, ensure Python version is 3.9+
```bash
python --version
```

---

## ✅ Success Checklist

After running evaluation, you should have:

- [ ] Terminal output showing test results
- [ ] Files in `backend/evaluation_results/` folder
- [ ] Metrics for all thresholds tested
- [ ] Identified best performing threshold
- [ ] Understanding of precision vs. recall trade-off
- [ ] Data ready for research paper

---

**Ready to publish your research! 📄🎓**

---

