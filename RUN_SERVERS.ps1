# ================================================================================
# AI Resume Screening System - Run Backend + Frontend Servers
# EmpowerTech Solutions
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "AI RESUME SCREENING SYSTEM - START SERVERS" -ForegroundColor Cyan
Write-Host "EmpowerTech Solutions" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# ================================================================================
# CHECK PYTHON
# ================================================================================

Write-Host "Checking Python installation..." -ForegroundColor Cyan

$pythonCmd = ""
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Python found: $pythonCmd" -ForegroundColor Green

# ================================================================================
# CHECK NODE.JS
# ================================================================================

Write-Host "Checking Node.js installation..." -ForegroundColor Cyan

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Node.js not found!" -ForegroundColor Red
    Write-Host "Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] npm not found!" -ForegroundColor Red
    Write-Host "Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$nodeVersion = node --version
$npmVersion = npm --version
Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
Write-Host "[OK] npm found: $npmVersion" -ForegroundColor Green

Write-Host ""

# ================================================================================
# CHECK DEPENDENCIES
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "CHECKING DEPENDENCIES" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

# Check backend dependencies
Write-Host "Checking backend dependencies..." -ForegroundColor Cyan
$flaskInstalled = & $pythonCmd -m pip show Flask 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Backend dependencies not installed" -ForegroundColor Yellow
    $installBackend = Read-Host "Install backend dependencies now? (y/n)"
    if ($installBackend -eq "y") {
        Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
        Set-Location backend
        & $pythonCmd -m pip install -r requirements.txt
        Set-Location ..
        Write-Host "[OK] Backend dependencies installed!" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Backend may not work without dependencies" -ForegroundColor Yellow
    }
} else {
    Write-Host "[OK] Backend dependencies found" -ForegroundColor Green
}

# Check frontend dependencies
Write-Host "Checking frontend dependencies..." -ForegroundColor Cyan
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[WARNING] Frontend dependencies not installed" -ForegroundColor Yellow
    $installFrontend = Read-Host "Install frontend dependencies now? (y/n)"
    if ($installFrontend -eq "y") {
        Write-Host "Installing frontend dependencies (this may take a few minutes)..." -ForegroundColor Cyan
        Set-Location frontend
        npm install
        Set-Location ..
        Write-Host "[OK] Frontend dependencies installed!" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Frontend will not work without dependencies" -ForegroundColor Yellow
    }
} else {
    Write-Host "[OK] Frontend dependencies found" -ForegroundColor Green
}

Write-Host ""

# ================================================================================
# CREATE .env FILE IF NEEDED
# ================================================================================

if (-not (Test-Path "backend\.env")) {
    Write-Host "Creating backend .env file..." -ForegroundColor Cyan
    if (Test-Path "backend\.env.example") {
        Copy-Item "backend\.env.example" "backend\.env"
        Write-Host "[OK] .env file created from .env.example" -ForegroundColor Green
    } else {
        # Create a basic .env file
        @"
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=True
"@ | Out-File -FilePath "backend\.env" -Encoding UTF8
        Write-Host "[OK] Basic .env file created" -ForegroundColor Green
    }
}

Write-Host ""

# ================================================================================
# START SERVERS
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STARTING SERVERS" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Starting Backend Flask Server (Port 5000)..." -ForegroundColor Yellow
Write-Host "Starting Frontend React Server (Port 3000)..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Both servers will open in new windows." -ForegroundColor Cyan
Write-Host "To stop servers: Close the terminal windows or press Ctrl+C in each" -ForegroundColor Cyan
Write-Host ""

# Start Backend in new PowerShell window
$backendScript = @"
cd '$PWD\backend'
Write-Host '================================================================================' -ForegroundColor Green
Write-Host 'BACKEND FLASK SERVER - PORT 5000' -ForegroundColor Green
Write-Host '================================================================================' -ForegroundColor Green
Write-Host ''
Write-Host 'Starting Flask server...' -ForegroundColor Cyan
Write-Host 'Access API at: http://localhost:5000' -ForegroundColor Yellow
Write-Host 'Press Ctrl+C to stop the server' -ForegroundColor Yellow
Write-Host ''
& $pythonCmd main.py
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

Write-Host "[OK] Backend server starting in new window..." -ForegroundColor Green
Start-Sleep -Seconds 2

# Start Frontend in new PowerShell window
$frontendScript = @"
cd '$PWD\frontend'
Write-Host '================================================================================' -ForegroundColor Cyan
Write-Host 'FRONTEND REACT SERVER - PORT 3000' -ForegroundColor Cyan
Write-Host '================================================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Starting React development server...' -ForegroundColor Cyan
Write-Host 'The app will open in your browser automatically' -ForegroundColor Yellow
Write-Host 'Press Ctrl+C to stop the server' -ForegroundColor Yellow
Write-Host ''
npm start
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "[OK] Frontend server starting in new window..." -ForegroundColor Green

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "SERVERS STARTED!" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Backend API:" -ForegroundColor Yellow
Write-Host "  URL: http://localhost:5000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:5000/api" -ForegroundColor White
Write-Host "  Health Check: http://localhost:5000/health" -ForegroundColor White
Write-Host ""

Write-Host "Frontend App:" -ForegroundColor Yellow
Write-Host "  URL: http://localhost:3000" -ForegroundColor White
Write-Host "  (Should open automatically in your browser)" -ForegroundColor Gray
Write-Host ""

Write-Host "The servers are running in separate windows." -ForegroundColor Cyan
Write-Host "To stop: Close the terminal windows or press Ctrl+C in each window" -ForegroundColor Cyan
Write-Host ""

Write-Host "Waiting 5 seconds before opening browser..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Open browser to frontend
Write-Host "Opening application in browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "READY TO USE!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Quick Links:" -ForegroundColor Yellow
Write-Host "  Dashboard: http://localhost:3000/" -ForegroundColor White
Write-Host "  Upload Resume: http://localhost:3000/upload" -ForegroundColor White
Write-Host "  Jobs: http://localhost:3000/jobs" -ForegroundColor White
Write-Host "  Match Results: http://localhost:3000/match" -ForegroundColor White
Write-Host "  Analytics: http://localhost:3000/analytics" -ForegroundColor White
Write-Host "  Evaluation: http://localhost:3000/evaluation" -ForegroundColor White
Write-Host ""

Write-Host "API Endpoints:" -ForegroundColor Yellow
Write-Host "  POST http://localhost:5000/api/resumes/upload - Upload resume" -ForegroundColor White
Write-Host "  GET  http://localhost:5000/api/resumes - List resumes" -ForegroundColor White
Write-Host "  GET  http://localhost:5000/api/jobs - List jobs" -ForegroundColor White
Write-Host "  POST http://localhost:5000/api/match - Match resumes to jobs" -ForegroundColor White
Write-Host ""

Write-Host "Keep this window open to see server status." -ForegroundColor Cyan
Write-Host "Check the other windows for server logs." -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to close this window (servers will continue running)"
