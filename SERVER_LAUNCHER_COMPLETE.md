# ✅ SERVER LAUNCHER COMPLETE!

## Run Backend + Frontend with One Command

---

## 🎯 **WHAT TO RUN**

### **Easiest: Double-Click**
```
Double-click: RUN_SERVERS.bat
```

### **PowerShell:**
```powershell
.\RUN_SERVERS.ps1
```

### **One-Liner:**
```powershell
Start-Process powershell -ArgumentList "-NoExit","-Command","cd backend; py main.py"; Start-Sleep 3; Start-Process powershell -ArgumentList "-NoExit","-Command","cd frontend; npm start"
```

---

## 🌐 **Access After Starting**

- **Frontend App:** http://localhost:3000 (auto-opens)
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/health

**Time to start:** ~10 seconds

---

## 📄 **NEW FILES CREATED**

1. ✅ **`RUN_SERVERS.ps1`** - PowerShell server launcher
2. ✅ **`RUN_SERVERS.bat`** - Batch server launcher
3. ✅ **`RUN_SERVERS_GUIDE.md`** - Complete guide
4. ✅ **`SERVER_LAUNCHER_COMPLETE.md`** - This summary

---

## ⚡ **What These Scripts Do**

1. ✅ Check Python installation
2. ✅ Check Node.js installation
3. ✅ Verify dependencies (install if missing)
4. ✅ Create .env file if needed
5. ✅ Start Backend Flask server (Port 5000)
6. ✅ Start Frontend React server (Port 3000)
7. ✅ Open browser automatically
8. ✅ Keep both servers running

**Both servers open in separate windows for easy monitoring!**

---

## 🔍 **Features**

### **Automatic Checks**
- Python installed?
- Node.js installed?
- Backend dependencies?
- Frontend dependencies?
- .env file exists?

### **Smart Installation**
- Offers to install missing dependencies
- Creates .env from .env.example
- Handles errors gracefully

### **Separate Windows**
- Backend in one window
- Frontend in another window
- Easy to see logs
- Easy to stop individually

### **Auto-Open**
- Browser opens to http://localhost:3000 automatically
- Ready to use in 10 seconds

---

## 📊 **All Available Scripts**

| Script | Purpose | When to Use |
|--------|---------|-------------|
| **`RUN_SERVERS.ps1`** | Start dev servers | **Daily development** ⭐ |
| **`RUN_SERVERS.bat`** | Start dev servers | **Daily development** ⭐ |
| `RUN_COMPLETE.ps1` | Generate dataset + evaluate | Research/testing |
| `RUN_COMPLETE.bat` | Generate dataset + evaluate | Research/testing |
| `run_high_accuracy.bat` | Run 10K evaluation | Publication prep |

---

## 🎯 **Quick Decision Guide**

### **Want to develop/test the app?**
→ **Run `RUN_SERVERS.bat`** (double-click)

### **Want to generate test data?**
→ Run `RUN_COMPLETE.bat` (double-click)

### **Want to do both?**
1. First: `RUN_SERVERS.bat` → Opens app
2. Then: In app, go to "Evaluation" page → Run tests

---

## 🛑 **How to Stop**

### **Option 1: Close Windows**
Close the "Backend Flask Server" and "Frontend React Server" windows

### **Option 2: Ctrl+C**
Press Ctrl+C in each window, then press Y

### **Option 3: Command**
```powershell
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

---

## 🚨 **Common Issues**

### **"Port already in use"**
Someone else is using port 5000 or 3000:

```powershell
# Kill processes on those ports
netstat -ano | findstr :5000
netstat -ano | findstr :3000
taskkill /PID [NUMBER] /F
```

### **"Python not found"**
Install Python: https://www.python.org/downloads/

### **"Node not found"**
Install Node.js: https://nodejs.org/

### **"Dependencies missing"**
```powershell
cd backend
py -m pip install -r requirements.txt

cd ..\frontend
npm install
```

---

## 💻 **Development Workflow**

### **Daily Development**

```powershell
# Morning: Start servers
.\RUN_SERVERS.ps1

# Develop: Edit code
# - Backend: Edit Python files in backend/
# - Frontend: Edit React files in frontend/src/

# Test: Automatic reload
# - Save files
# - Servers auto-reload
# - Refresh browser if needed

# Evening: Stop servers
# Close the server windows or Ctrl+C
```

### **Features During Development**

- ✅ **Auto-reload:** Both servers reload on file changes
- ✅ **Debug mode:** See detailed errors
- ✅ **Hot module replacement:** Frontend updates without full reload
- ✅ **Source maps:** Debug original code, not transpiled

---

## 📱 **Quick Test Commands**

### **Test Backend**
```powershell
# Health check
Invoke-RestMethod http://localhost:5000/health

# List resumes
Invoke-RestMethod http://localhost:5000/api/resumes

# List jobs
Invoke-RestMethod http://localhost:5000/api/jobs
```

### **Test Frontend**
Just open http://localhost:3000 and navigate:
- Dashboard
- Upload Resume
- Jobs
- Match Results
- Analytics
- Evaluation

---

## 🎓 **For Development**

### **Backend Development (Flask/Python)**

**Location:** `backend/`

**Main file:** `backend/main.py`

**Edit files:**
- `backend/app/routes/*.py` - API endpoints
- `backend/app/services/*.py` - Business logic
- `backend/app/models/*.py` - ML algorithms
- `backend/app/utils/*.py` - Utilities

**Auto-reload:** Yes (when files saved)

### **Frontend Development (React/JavaScript)**

**Location:** `frontend/`

**Main file:** `frontend/src/App.js`

**Edit files:**
- `frontend/src/pages/*.js` - Page components
- `frontend/src/components/*.js` - Reusable components
- `frontend/src/services/api.js` - API calls
- `frontend/src/*.css` - Styles

**Auto-reload:** Yes (hot module replacement)

---

## 🔧 **Configuration**

### **Backend Configuration**

**File:** `backend/.env`

```env
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=True
```

**Change port:**
Edit `backend/main.py`, line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000
```

### **Frontend Configuration**

**File:** `frontend/.env` (create if needed)

```env
PORT=3000
REACT_APP_API_URL=http://localhost:5000
```

---

## 📊 **What Runs**

### **Backend Process**
```
Python Flask Server
Port: 5000
Auto-reload: Enabled
Debug: Enabled
CORS: Enabled (for frontend)
```

### **Frontend Process**
```
React Development Server
Port: 3000
Auto-reload: Enabled (HMR)
Source maps: Enabled
Proxy to backend: Configured
```

---

## ✅ **Success Indicators**

After running `RUN_SERVERS`:

### **Backend Window Shows:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

### **Frontend Window Shows:**
```
Compiled successfully!
You can now view frontend in the browser.
  Local: http://localhost:3000
```

### **Browser Opens:**
- Dashboard loads
- No console errors
- Can navigate pages

---

## 🎯 **Complete Project Setup**

### **First Time Setup (One-Time)**

1. **Clone/Download project**
2. **Install dependencies:**
   ```powershell
   cd backend
   py -m pip install -r requirements.txt
   cd ..\frontend
   npm install
   ```

### **Daily Development**

1. **Start servers:** `.\RUN_SERVERS.ps1`
2. **Develop:** Edit code
3. **Test:** Use the app
4. **Stop:** Close windows when done

### **Research/Testing**

1. **Generate data:** `.\RUN_COMPLETE.ps1`
2. **Or use app:** Start servers → Go to Evaluation page

---

## 📚 **Documentation**

- **`RUN_SERVERS_GUIDE.md`** - Complete server guide
- **`COMPLETE_AUTOMATION_GUIDE.md`** - Full automation guide
- **`DEVELOPER_GUIDE.md`** - Code development guide
- **`WINDOWS_FIX_COMPLETE.md`** - Windows troubleshooting

---

## 🎉 **Summary**

**You now have:**

✅ **One-click server startup** - `RUN_SERVERS.bat`  
✅ **PowerShell script** - `RUN_SERVERS.ps1`  
✅ **Auto dependency check** - Installs if missing  
✅ **Separate server windows** - Easy monitoring  
✅ **Auto-open browser** - Ready in 10 seconds  
✅ **Complete documentation** - Full guides  

**From zero to running app in ONE command!**

---

## 🚀 **START NOW**

```powershell
# Navigate to project
cd "C:\Users\DipeshNagpal\Repos\Resume screening"

# Start servers
.\RUN_SERVERS.ps1
```

**Or just double-click: `RUN_SERVERS.bat`**

**That's it!** ✅

---

**EmpowerTech Solutions**  
Chennai, Tamil Nadu, India

*Development made easy - One command to run everything!* 🚀

**Version:** 6.0.0 - Server Launcher Edition  
**Date:** December 2024
