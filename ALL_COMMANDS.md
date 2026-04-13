# 🎯 ALL COMMANDS - Master Index

## Every Script & Command in One Place

**EmpowerTech Solutions - Complete Reference**

---

## 🚀 **MOST COMMON (Use These 90% of the Time)**

### **1. Start Development Servers** ⭐⭐⭐
```powershell
.\RUN_SERVERS.ps1
```
**Or double-click:** `RUN_SERVERS.bat`

**Opens:** Backend (5000) + Frontend (3000)  
**Use for:** Daily development, testing features

### **2. Generate 10K Test Cases + Evaluate** ⭐⭐
```powershell
.\RUN_COMPLETE.ps1
```
**Or double-click:** `RUN_COMPLETE.bat`

**Generates:** 10,000 test cases + Full evaluation  
**Use for:** Research, publication results

---

## 📁 **ALL AVAILABLE SCRIPTS**

| Script | Purpose | Time | Output |
|--------|---------|------|--------|
| **`RUN_SERVERS.ps1`** | Start dev servers | 10s | App running |
| **`RUN_SERVERS.bat`** | Start dev servers | 10s | App running |
| **`RUN_COMPLETE.ps1`** | Full automation | 6-50 min | Research results |
| **`RUN_COMPLETE.bat`** | Full automation | 6-50 min | Research results |
| `run_high_accuracy.bat` | High-accuracy eval | 6 min | 10K results |
| `run_high_accuracy_workflow.py` | Python workflow | 6 min | 10K results |

---

## 💻 **DEVELOPMENT COMMANDS**

### **Start Servers (Combined)**
```powershell
# PowerShell
.\RUN_SERVERS.ps1

# Batch
RUN_SERVERS.bat

# One-liner
Start-Process powershell -ArgumentList "-NoExit","-Command","cd backend; py main.py"; Start-Sleep 3; Start-Process powershell -ArgumentList "-NoExit","-Command","cd frontend; npm start"
```

### **Start Backend Only**
```powershell
cd backend
py main.py
```

### **Start Frontend Only**
```powershell
cd frontend
npm start
```

### **Stop All Servers**
```powershell
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

---

## 📊 **RESEARCH/EVALUATION COMMANDS**

### **Complete Workflow (10K)**
```powershell
.\RUN_COMPLETE.ps1
# Select option 2 (10,000 cases)
```

### **Quick Test (1K)**
```powershell
.\RUN_COMPLETE.ps1
# Select option 1 (1,000 cases)
```

### **Research Grade (100K)**
```powershell
.\RUN_COMPLETE.ps1
# Select option 4 (100,000 cases)
```

### **Individual Steps**

**Generate Dataset:**
```powershell
py generate_synthetic_dataset.py --size 10000
```

**Run Evaluation:**
```powershell
py run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --compare
```

**Generate Charts:**
```powershell
py generate_visualizations.py
```

**Run Cross-Validation:**
```powershell
py run_cross_validation.py --k 5 --threshold 0.5
```

---

## 🔧 **INSTALLATION COMMANDS**

### **First Time Setup**

**Backend:**
```powershell
cd backend
py -m pip install -r requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install
```

**Both:**
```powershell
cd backend
py -m pip install -r requirements.txt
cd ..\frontend
npm install
cd ..
```

### **Update Dependencies**

**Backend:**
```powershell
cd backend
py -m pip install -r requirements.txt --upgrade
```

**Frontend:**
```powershell
cd frontend
npm update
```

---

## 🧪 **TESTING COMMANDS**

### **Test Backend Health**
```powershell
Invoke-RestMethod http://localhost:5000/health
```

### **List Resumes**
```powershell
Invoke-RestMethod http://localhost:5000/api/resumes
```

### **List Jobs**
```powershell
Invoke-RestMethod http://localhost:5000/api/jobs
```

### **Run Evaluation Test**
```powershell
Invoke-RestMethod -Method POST http://localhost:5000/api/evaluation/run-test
```

### **Frontend Navigation**
- Dashboard: http://localhost:3000/
- Upload: http://localhost:3000/upload
- Jobs: http://localhost:3000/jobs
- Match: http://localhost:3000/match
- Analytics: http://localhost:3000/analytics
- Evaluation: http://localhost:3000/evaluation

---

## 📦 **BUILD COMMANDS**

### **Backend Production**
```powershell
cd backend
py -m pip install gunicorn
gunicorn -w 4 main:app
```

### **Frontend Production**
```powershell
cd frontend
npm run build
```

Build output: `frontend/build/`

---

## 🗄️ **DATABASE COMMANDS**

### **Check Database**
```powershell
# Database file location
ls backend\database\resume_screening.db

# View with SQLite (if installed)
sqlite3 backend\database\resume_screening.db
```

### **Reset Database**
```powershell
# Backup first!
copy backend\database\resume_screening.db backend\database\backup.db

# Delete to reset
del backend\database\resume_screening.db
```

---

## 📊 **RESULTS & OUTPUT COMMANDS**

### **View Latest Results**
```powershell
# Latest comparison
$latest = Get-ChildItem backend\evaluation_results\large_comparison_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content $latest.FullName | ConvertFrom-Json | Format-List
```

### **Open Results Folder**
```powershell
start backend\evaluation_results
```

### **Open Visualizations**
```powershell
start visualizations
```

### **View Dataset Info**
```powershell
$data = Get-Content backend\data\large_test_dataset.json | ConvertFrom-Json
Write-Host "Total cases: $($data.total_cases)"
Write-Host "Positive: $($data.positive_cases)"
Write-Host "Negative: $($data.negative_cases)"
```

---

## 🔍 **DIAGNOSTIC COMMANDS**

### **Check Python**
```powershell
py --version
python --version
python3 --version
```

### **Check Node.js**
```powershell
node --version
npm --version
```

### **Check Installed Packages**

**Backend:**
```powershell
py -m pip list
py -m pip show Flask scikit-learn numpy pandas matplotlib
```

**Frontend:**
```powershell
cd frontend
npm list
```

### **Check Ports in Use**
```powershell
# Check port 5000 (backend)
netstat -ano | findstr :5000

# Check port 3000 (frontend)
netstat -ano | findstr :3000
```

---

## 🛠️ **TROUBLESHOOTING COMMANDS**

### **Fix lxml Import Error** ⭐
```powershell
.\FIX_LXML_ERROR.ps1
```
**Or double-click:** `FIX_LXML_ERROR.bat`

**Fixes:** Backend crash with "cannot import name 'etree' from 'lxml'"

### **Fix Empty Visualizations** ⭐
**Problem:** Visualizations folder is empty after running RUN_COMPLETE.ps1

**Solution:** Now fixed automatically! The script now searches for both:
- `comparison_*.json` files (from run_comparative_evaluation.py)
- `large_comparison_*.json` files (from run_large_scale_evaluation.py)

**Manual regeneration:**
```powershell
py generate_visualizations.py
```

**Verify fix:**
```powershell
ls visualizations\*.png
```
Should show 5 PNG files.

**Read:** `VISUALIZATION_FIX_COMPLETE.md` for details

### **Fix Port Conflicts**
```powershell
# Kill process on port 5000
$port5000 = netstat -ano | findstr :5000
# Extract PID and kill
taskkill /PID [PID_NUMBER] /F

# Kill process on port 3000
$port3000 = netstat -ano | findstr :3000
taskkill /PID [PID_NUMBER] /F
```

### **Clear Cache**

**Backend:**
```powershell
# Clear Python cache
Get-ChildItem -Path backend -Include __pycache__ -Recurse | Remove-Item -Recurse -Force
```

**Frontend:**
```powershell
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

### **Reset Everything**
```powershell
# Backend
cd backend
py -m pip uninstall -r requirements.txt -y
py -m pip install -r requirements.txt

# Frontend
cd ..\frontend
rmdir /s /q node_modules
npm install

cd ..
```

---

## 📝 **UTILITY COMMANDS**

### **Count Lines of Code**
```powershell
# Python
(Get-ChildItem -Path backend -Include *.py -Recurse | Get-Content).Count

# JavaScript
(Get-ChildItem -Path frontend\src -Include *.js,*.jsx -Recurse | Get-Content).Count
```

### **Search Code**
```powershell
# Search in backend
Get-ChildItem -Path backend -Include *.py -Recurse | Select-String "search_term"

# Search in frontend
Get-ChildItem -Path frontend\src -Include *.js -Recurse | Select-String "search_term"
```

### **Git Commands**
```powershell
# Status
git status

# Add all
git add .

# Commit
git commit -m "Your message"

# Push
git push
```

---

## 🎓 **RESEARCH COMMANDS**

### **Quick Evaluation (1K)**
```powershell
py generate_synthetic_dataset.py --size 1000
py run_large_scale_evaluation.py --sample 1000 --compare
```

### **Standard Evaluation (10K)**
```powershell
py generate_synthetic_dataset.py --size 10000
py run_large_scale_evaluation.py --compare
py generate_visualizations.py
```

### **Publication Grade (100K)**
```powershell
py generate_synthetic_dataset.py --size 100000
py run_large_scale_evaluation.py --compare
py generate_visualizations.py
```

### **With Cross-Validation**
```powershell
py generate_synthetic_dataset.py --size 10000
py run_large_scale_evaluation.py --compare
py run_cross_validation.py --k 5
py generate_visualizations.py
```

---

## 📂 **FILE OPERATIONS**

### **Backup Results**
```powershell
$date = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item -Path backend\evaluation_results -Destination "backup_results_$date" -Recurse
```

### **Export Results to CSV**
```powershell
$results = Get-Content backend\evaluation_results\large_comparison_*.json | ConvertFrom-Json
$results | ConvertTo-Csv | Out-File results.csv
```

### **Compress Results**
```powershell
Compress-Archive -Path backend\evaluation_results\* -DestinationPath "results_$(Get-Date -Format 'yyyyMMdd').zip"
```

---

## 🎯 **QUICK REFERENCE TABLE**

| Task | Command |
|------|---------|
| **Start developing** | `.\RUN_SERVERS.ps1` |
| **Run research** | `.\RUN_COMPLETE.ps1` |
| **Test 1K cases** | Option 1 in RUN_COMPLETE |
| **Test 10K cases** | Option 2 in RUN_COMPLETE |
| **Backend only** | `cd backend; py main.py` |
| **Frontend only** | `cd frontend; npm start` |
| **Stop all** | `taskkill /F /IM python.exe; taskkill /F /IM node.exe` |
| **Install deps** | `cd backend; py -m pip install -r requirements.txt; cd ..\frontend; npm install` |
| **View results** | `start backend\evaluation_results` |
| **Open app** | http://localhost:3000 |
| **API health** | http://localhost:5000/health |

---

## 📚 **DOCUMENTATION COMMANDS**

### **View Documentation**
```powershell
# Open in default editor
notepad README.md
notepad COMPLETE_AUTOMATION_GUIDE.md
notepad RUN_SERVERS_GUIDE.md
```

### **List All Docs**
```powershell
Get-ChildItem -Filter "*.md" | Select-Object Name, Length, LastWriteTime
```

---

## 🎉 **MOST USED WORKFLOW**

### **Daily Development**
```powershell
# 1. Start servers
.\RUN_SERVERS.ps1

# 2. Edit code in Visual Studio
# - Backend: backend/app/**/*.py
# - Frontend: frontend/src/**/*.js

# 3. Test in browser
# http://localhost:3000

# 4. Stop when done
# Close server windows or Ctrl+C
```

### **Research Work**
```powershell
# 1. Generate and evaluate
.\RUN_COMPLETE.ps1
# Select option 2 (10,000 cases)

# 2. Wait ~6 minutes

# 3. Review results
start backend\evaluation_results
start visualizations

# 4. Insert into paper
# Open docs\RESEARCH_PAPER_TEMPLATE.md
```

---

**EmpowerTech Solutions**  
Chennai, Tamil Nadu, India

**Master Index of All Commands - Keep this handy!** 📚✨

**Last Updated:** December 2024
