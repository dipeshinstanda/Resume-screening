# 🚀 RUN SERVERS - Quick Reference

## Start Backend + Frontend Servers

---

## ⚡ **QUICK START (3 Methods)**

### **Method 1: Double-Click (Easiest!)**

1. Open File Explorer
2. Navigate to: `C:\Users\DipeshNagpal\Repos\Resume screening\`
3. **Double-click:** `RUN_SERVERS.bat`
4. Wait ~10 seconds
5. Browser opens automatically!

### **Method 2: PowerShell**

```powershell
cd "C:\Users\DipeshNagpal\Repos\Resume screening"
.\RUN_SERVERS.ps1
```

### **Method 3: One-Line Command**

**PowerShell:**
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; py main.py"; Start-Sleep 3; Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"
```

**Command Prompt:**
```cmd
start cmd /k "cd backend && py main.py" && timeout /t 3 && start cmd /k "cd frontend && npm start"
```

---

## 🌐 **Access Points**

After servers start (~10 seconds):

### **Frontend (React App)**
- **URL:** http://localhost:3000
- **Opens automatically in browser**

### **Backend (Flask API)**
- **URL:** http://localhost:5000
- **Health Check:** http://localhost:5000/health
- **API Base:** http://localhost:5000/api

---

## 📁 **Available Pages**

Once the frontend loads:

- **Dashboard:** http://localhost:3000/
- **Upload Resume:** http://localhost:3000/upload
- **Job Management:** http://localhost:3000/jobs
- **Match Results:** http://localhost:3000/match
- **Analytics:** http://localhost:3000/analytics
- **Evaluation:** http://localhost:3000/evaluation

---

## 🔧 **API Endpoints**

Test backend directly:

### **Resumes**
```powershell
# List all resumes
Invoke-RestMethod http://localhost:5000/api/resumes

# Upload resume (requires file)
$file = Get-Item "path\to\resume.pdf"
# Use frontend UI for uploads
```

### **Jobs**
```powershell
# List all jobs
Invoke-RestMethod http://localhost:5000/api/jobs

# Create job
$body = @{
    title = "Software Engineer"
    description = "Looking for experienced developer"
    requirements = @("Bachelors in CS", "3+ years experience")
    education_requirements = @("Bachelors in Computer Science")
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri http://localhost:5000/api/jobs -Body $body -ContentType "application/json"
```

### **Matching**
```powershell
# Match resumes to job
$body = @{
    job_id = "job_id_here"
    threshold = 0.5
} | ConvertTo-Json

Invoke-RestMethod -Method POST -Uri http://localhost:5000/api/match -Body $body -ContentType "application/json"
```

---

## 🛑 **Stop Servers**

### **Option 1: Close Windows**
- Close the "Backend Flask Server" window
- Close the "Frontend React Server" window

### **Option 2: Ctrl+C**
- Press `Ctrl+C` in each server window
- Confirm with `Y` when prompted

### **Option 3: Kill Processes**

**PowerShell:**
```powershell
# Stop backend
Get-Process | Where-Object {$_.ProcessName -match "python"} | Stop-Process

# Stop frontend
Get-Process | Where-Object {$_.ProcessName -match "node"} | Stop-Process
```

**Command Prompt:**
```cmd
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

---

## 🚨 **Troubleshooting**

### **Port Already in Use**

If you get "Address already in use" error:

**Backend (Port 5000):**
```powershell
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F
```

**Frontend (Port 3000):**
```powershell
# Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID [PID_NUMBER] /F
```

### **Backend Dependencies Missing**

```powershell
cd backend
py -m pip install -r requirements.txt
```

### **Frontend Dependencies Missing**

```powershell
cd frontend
npm install
```

### **Backend Won't Start**

Check if .env file exists:
```powershell
# Create from example
copy backend\.env.example backend\.env
```

### **Frontend Won't Start**

Clear cache and reinstall:
```powershell
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

---

## ⚙️ **Configuration**

### **Backend (Flask)**

**File:** `backend/.env`

```env
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=True
```

**Port:** 5000 (default)

To change port, edit `backend/main.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change port here
```

### **Frontend (React)**

**Port:** 3000 (default)

To change port, create `frontend/.env`:
```env
PORT=3001
```

---

## 📊 **Development vs Production**

### **Development (Current)**
- **Backend:** Flask debug mode ON
- **Frontend:** React dev server
- **Auto-reload:** Yes
- **Source maps:** Yes
- **Performance:** Slower (but easier to debug)

### **Production**

**Backend:**
```powershell
cd backend
py -m pip install gunicorn
gunicorn -w 4 main:app
```

**Frontend:**
```powershell
cd frontend
npm run build
# Serve build folder with nginx or similar
```

---

## 🔄 **Auto-Restart on Changes**

Both servers auto-reload when you save files:

- **Backend:** Flask auto-reloads when Python files change
- **Frontend:** React auto-reloads when JS/CSS files change

Just save your changes and refresh the browser!

---

## 📝 **Quick Test**

After starting servers:

**Test Backend:**
```powershell
Invoke-RestMethod http://localhost:5000/health
```

**Expected:**
```json
{
  "status": "healthy"
}
```

**Test Frontend:**
Open http://localhost:3000 in browser - Should see Dashboard

---

## 💡 **Pro Tips**

### **Keep Servers Running**
Leave the server windows open while developing. They'll auto-reload on file changes.

### **Check Logs**
- **Backend logs:** See Flask server window
- **Frontend logs:** See React server window
- **Browser console:** F12 → Console tab

### **Debug Mode**
Backend runs in debug mode by default:
- Detailed error messages
- Auto-reload on code changes
- Interactive debugger

### **Environment Variables**
Create `backend/.env` for configuration:
```env
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///database/resume_screening.db
```

---

## 🎯 **Common Development Workflow**

1. **Start servers:**
   ```powershell
   .\RUN_SERVERS.ps1
   ```

2. **Make code changes:**
   - Edit backend Python files
   - Edit frontend React files

3. **Test changes:**
   - Backend auto-reloads
   - Frontend auto-reloads
   - Refresh browser if needed

4. **Stop servers when done:**
   - Press Ctrl+C in each window
   - Or close the windows

5. **Next day:**
   - Run `.\RUN_SERVERS.ps1` again
   - Continue development

---

## 🆚 **Comparison: Scripts**

| Script | Purpose | Use When |
|--------|---------|----------|
| `RUN_SERVERS.ps1` | Start backend + frontend | **Daily development** |
| `RUN_COMPLETE.ps1` | Generate dataset + evaluate | **Research/testing** |
| `run_high_accuracy.bat` | Run 10K evaluation | **Publication prep** |

---

## ✅ **Success Checklist**

After running `RUN_SERVERS`:

- [ ] Backend window opens showing Flask startup
- [ ] Frontend window opens showing React compilation
- [ ] Browser opens to http://localhost:3000
- [ ] Dashboard page loads
- [ ] Can navigate to different pages
- [ ] Backend responds at http://localhost:5000/health

---

## 📞 **Need Help?**

### **Servers Won't Start**
1. Check Python installed: `py --version`
2. Check Node installed: `node --version`
3. Install dependencies:
   ```powershell
   cd backend; py -m pip install -r requirements.txt; cd ..
   cd frontend; npm install; cd ..
   ```

### **Port Conflicts**
Kill existing processes:
```powershell
# Kill all Python and Node processes
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

### **Still Issues**
See full guides:
- `COMPLETE_AUTOMATION_GUIDE.md`
- `WINDOWS_FIX_COMPLETE.md`

---

**EmpowerTech Solutions**  
Chennai, Tamil Nadu, India

**Quick Commands:**
- **Start:** `.\RUN_SERVERS.ps1` or double-click `RUN_SERVERS.bat`
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000
- **Stop:** Ctrl+C in server windows
