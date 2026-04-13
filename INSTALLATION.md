# Installation Instructions

## AI-Based Resume Screening System
**EmpowerTech Solutions**

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Python 3.9 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: `python --version`

2. **Node.js 16 or higher and npm**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **pip (Python package manager)**
   - Usually comes with Python
   - Verify: `pip --version`

## Installation Steps

### Step 1: Install Backend Dependencies

1. Open a terminal/command prompt

2. Navigate to the backend directory:
```bash
cd backend
```

3. Install Python packages:
```bash
pip install -r requirements.txt
```

**Note for Windows users:** If you encounter permission errors, try:
```bash
pip install -r requirements.txt --user
```

**Note for Mac/Linux users:** You might need to use `pip3`:
```bash
pip3 install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

1. Open a new terminal/command prompt

2. Navigate to the frontend directory:
```bash
cd frontend
```

3. Install npm packages:
```bash
npm install
```

This may take a few minutes to complete.

### Step 3: Verify Installation

#### Verify Backend

```bash
cd backend
python main.py
```

You should see:
```
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
```

Press `Ctrl+C` to stop the server.

#### Verify Frontend

```bash
cd frontend
npm start
```

The application should open in your browser at `http://localhost:3000`

Press `Ctrl+C` to stop the development server.

## Running the Application

### Method 1: Manual Start (Recommended for first-time setup)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Method 2: Using VS Code Tasks

1. Open the project in Visual Studio Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Tasks: Run Task"
4. Select "Start Full Application"

This will start both backend and frontend in separate terminals.

## Common Issues and Solutions

### Issue: Python not found

**Solution:**
- Ensure Python is installed and added to PATH
- On Windows, try using `py` instead of `python`:
  ```bash
  py main.py
  ```

### Issue: pip not found

**Solution:**
- Try using `python -m pip` instead:
  ```bash
  python -m pip install -r requirements.txt
  ```

### Issue: Permission denied (Windows)

**Solution:**
- Run terminal as Administrator
- Or use `--user` flag:
  ```bash
  pip install -r requirements.txt --user
  ```

### Issue: Port 5000 already in use

**Solution:**
- Find and stop the process using port 5000
- Windows:
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID <process_id> /F
  ```
- Mac/Linux:
  ```bash
  lsof -i :5000
  kill -9 <process_id>
  ```

### Issue: Port 3000 already in use

**Solution:**
- The frontend will prompt you to use a different port
- Type 'Y' to use port 3001 instead

### Issue: npm install fails with network errors

**Solution:**
- Clear npm cache:
  ```bash
  npm cache clean --force
  ```
- Try again:
  ```bash
  npm install
  ```

### Issue: Module not found errors in Python

**Solution:**
- Ensure you're in the correct directory
- Reinstall requirements:
  ```bash
  cd backend
  pip install -r requirements.txt --upgrade
  ```

## Environment Configuration (Optional)

The backend includes a `.env.example` file. To use custom configuration:

1. Copy `.env.example` to `.env`:
```bash
cd backend
cp .env.example .env
```

2. Edit `.env` to customize settings (optional)

## Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend starts without errors (`python main.py`)
- [ ] Frontend starts without errors (`npm start`)
- [ ] Can access frontend at http://localhost:3000
- [ ] Can access backend API at http://localhost:5000

## Next Steps

Once installation is complete, refer to:
- [QUICKSTART.md](QUICKSTART.md) for a quick tutorial
- [README.md](README.md) for detailed documentation
- [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for API reference

## Support

If you encounter issues not covered here:
1. Check the error message carefully
2. Ensure all prerequisites are installed
3. Try reinstalling dependencies
4. Check that no other applications are using ports 3000 or 5000

---

