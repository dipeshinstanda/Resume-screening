# 🚀 Windows Quick Start

## Run High-Accuracy Evaluation on Windows

---

## ✅ **Step 1: Verify Python Installation**

Open PowerShell and run:

```powershell
py --version
```

**Expected:** `Python 3.9.x` or higher

If not installed:
1. Download from: https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart PowerShell

---

## ✅ **Step 2: Install Dependencies**

```powershell
cd "C:\Users\DipeshNagpal\Repos\Resume screening"
cd backend
py -m pip install -r requirements.txt
```

**Wait for completion** (~2 minutes)

---

## ✅ **Step 3: Install matplotlib**

```powershell
py -m pip install matplotlib
```

---

## ✅ **Step 4: Run High-Accuracy Workflow**

```powershell
cd "C:\Users\DipeshNagpal\Repos\Resume screening"
py run_high_accuracy_workflow.py
```

**OR run individual steps:**

### Generate 10K Dataset

```powershell
py generate_synthetic_dataset.py --size 10000
```

### Evaluate Enhanced ML

```powershell
py run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --enhanced
```

### Compare Algorithms

```powershell
py run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --compare
```

### Generate Visualizations

```powershell
py generate_visualizations.py
```

---

## ⚡ **Quick Test (1000 cases)**

Before running full 10K, test with 1000:

```powershell
# Generate 1000 test cases
py generate_synthetic_dataset.py --size 1000

# Evaluate and compare
py run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --sample 1000 --compare
```

**Time:** ~1 minute  
**Result:** Quick accuracy check

---

## 🔍 **Check Results**

```powershell
# View latest comparison results
py -c "import json, glob, os; files=glob.glob('backend/evaluation_results/large_comparison_*.json'); latest=max(files, key=os.path.getctime); data=json.load(open(latest)); print(f'Enhanced ML Accuracy: {data[\"enhanced_ml\"][\"accuracy\"]:.2%}'); print(f'Baseline Accuracy: {data[\"baseline\"][\"accuracy\"]:.2%}'); print(f'Improvement: +{(data[\"enhanced_ml\"][\"accuracy\"]-data[\"baseline\"][\"accuracy\"])*100:.1f}%')"
```

---

## 📊 **Expected Output**

```
Enhanced ML Accuracy: 89.50%
Baseline Accuracy: 77.50%
Improvement: +12.0%
```

---

## 🚨 **Troubleshooting**

### Error: "py is not recognized"

**Solution 1:** Use full path
```powershell
C:\Users\DipeshNagpal\AppData\Local\Programs\Python\Python39\python.exe --version
```

**Solution 2:** Add Python to PATH
1. Search for "Environment Variables" in Windows
2. Edit PATH
3. Add: `C:\Users\DipeshNagpal\AppData\Local\Programs\Python\Python39\`
4. Restart PowerShell

### Error: "No module named 'sklearn'"

```powershell
cd backend
py -m pip install -r requirements.txt --force-reinstall
```

### Error: "ModuleNotFoundError: No module named 'matplotlib'"

```powershell
py -m pip install matplotlib
```

### Error: "Permission denied"

Run PowerShell as Administrator:
1. Right-click PowerShell
2. Select "Run as Administrator"
3. Navigate to project folder
4. Run commands

---

## ✅ **Verification Checklist**

- [ ] `py --version` shows Python 3.9+
- [ ] `py -m pip list` includes: Flask, scikit-learn, numpy, pandas, matplotlib
- [ ] Can run: `py generate_synthetic_dataset.py --size 100`
- [ ] File created: `backend/data/large_test_dataset.json`
- [ ] Results appear in: `backend/evaluation_results/`

---

## 📁 **Expected Files After Running**

```
backend/data/
└── large_test_dataset.json (created, ~20 MB for 10K cases)

backend/evaluation_results/
├── large_eval_10000_*.json (Enhanced ML results)
└── large_comparison_10000_*.json (Comparison results)

visualizations/
├── comparison_chart.png
├── improvement_chart.png
├── confusion_matrices.png
├── threshold_analysis.png
└── score_distribution.png
```

---

## 🎯 **Next Steps After Success**

1. **Review Results:**
   - Open `backend/evaluation_results/large_comparison_*.json`
   - Note accuracy, precision, recall, F1-score

2. **View Charts:**
   - Open `visualizations/` folder
   - View PNG files

3. **Update Research Paper:**
   - Open `docs/RESEARCH_PAPER_TEMPLATE.md`
   - Insert metrics from results

4. **Cite in Paper:**
   ```
   "Evaluated on 10,000 diverse test cases, achieving 89.5% accuracy..."
   ```

---

## 💡 **Pro Tips**

### Run in Background
```powershell
Start-Process py -ArgumentList "run_high_accuracy_workflow.py" -NoNewWindow
```

### Save Output to Log
```powershell
py run_high_accuracy_workflow.py > output.log 2>&1
```

### Check Progress
```powershell
Get-Content output.log -Wait
```

---

## ⏱️ **Time Estimates**

| Task | 1K cases | 10K cases | 50K cases |
|------|----------|-----------|-----------|
| Generation | 10s | 2 min | 10 min |
| Evaluation | 8s | 1.5 min | 7 min |
| Visualization | 5s | 5s | 10s |
| **Total** | **~30s** | **~4 min** | **~18 min** |

---

## 🆘 **Still Having Issues?**

### Option 1: Use Python from Visual Studio

If you have Visual Studio with Python workload:

```powershell
# Find VS Python
& "C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\Extensions\Microsoft\Python\Core\python.exe" --version

# Use it directly
& "C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\Extensions\Microsoft\Python\Core\python.exe" run_high_accuracy_workflow.py
```

### Option 2: Install Python via Microsoft Store

1. Open Microsoft Store
2. Search "Python 3.11"
3. Install
4. Restart PowerShell
5. Use `python` or `py`

### Option 3: Use Anaconda

```powershell
conda create -n resume-screening python=3.9
conda activate resume-screening
pip install -r backend/requirements.txt
python run_high_accuracy_workflow.py
```

---

## 📞 **Support**

If still stuck, check:
1. Python installed? `py --version`
2. Dependencies installed? `py -m pip list`
3. In correct directory? `pwd` should show Resume screening folder
4. Files exist? `ls generate_synthetic_dataset.py`

---

*Windows-specific guide for high-accuracy evaluation* 🪟✨
