@echo off
setlocal

:: ================================================================================
:: AI Resume Screening System - Run Backend + Frontend Servers
:: EmpowerTech Solutions
:: ================================================================================

color 0B
echo ================================================================================
echo AI RESUME SCREENING SYSTEM - START SERVERS
echo EmpowerTech Solutions
echo ================================================================================
echo.

:: Check Python
echo Checking Python installation...
set PYTHON_CMD=
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo [OK] Python Launcher found
    goto :python_found
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo [OK] Python found
    goto :python_found
)

echo [ERROR] Python not found!
echo Please install from: https://www.python.org/downloads/
pause
exit /b 1

:python_found

:: Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    echo Please install from: https://nodejs.org/
    pause
    exit /b 1
)

npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found!
    echo Please install from: https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Node.js found
echo [OK] npm found
echo.

:: Check backend dependencies
echo ================================================================================
echo CHECKING DEPENDENCIES
echo ================================================================================
echo.

echo Checking backend dependencies...
%PYTHON_CMD% -m pip show Flask >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Backend dependencies not installed
    set /p install_backend="Install backend dependencies now? (y/n): "
    if /i "!install_backend!"=="y" (
        echo Installing backend dependencies...
        cd backend
        %PYTHON_CMD% -m pip install -r requirements.txt
        cd ..
        echo [OK] Backend dependencies installed!
    )
) else (
    echo [OK] Backend dependencies found
)

:: Check frontend dependencies
echo Checking frontend dependencies...
if not exist "frontend\node_modules" (
    echo [WARNING] Frontend dependencies not installed
    set /p install_frontend="Install frontend dependencies now? (y/n): "
    if /i "!install_frontend!"=="y" (
        echo Installing frontend dependencies...
        cd frontend
        call npm install
        cd ..
        echo [OK] Frontend dependencies installed!
    )
) else (
    echo [OK] Frontend dependencies found
)

echo.

:: Create .env if needed
if not exist "backend\.env" (
    echo Creating backend .env file...
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env" >nul
        echo [OK] .env file created
    )
)

:: Start servers
echo ================================================================================
echo STARTING SERVERS
echo ================================================================================
echo.

echo Starting Backend Flask Server (Port 5000)...
echo Starting Frontend React Server (Port 3000)...
echo.
echo Both servers will open in new windows.
echo To stop servers: Close the terminal windows or press Ctrl+C in each
echo.

:: Start Backend in new window
start "Backend Flask Server - Port 5000" cmd /k "cd /d "%CD%\backend" && echo ================================================================================ && echo BACKEND FLASK SERVER - PORT 5000 && echo ================================================================================ && echo. && echo Access API at: http://localhost:5000 && echo Press Ctrl+C to stop the server && echo. && %PYTHON_CMD% main.py"

:: Wait a bit for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend in new window
start "Frontend React Server - Port 3000" cmd /k "cd /d "%CD%\frontend" && echo ================================================================================ && echo FRONTEND REACT SERVER - PORT 3000 && echo ================================================================================ && echo. && echo The app will open in your browser automatically && echo Press Ctrl+C to stop the server && echo. && npm start"

echo.
echo ================================================================================
echo SERVERS STARTED!
echo ================================================================================
echo.

echo Backend API:
echo   URL: http://localhost:5000
echo   Health Check: http://localhost:5000/health
echo.

echo Frontend App:
echo   URL: http://localhost:3000
echo   (Should open automatically in your browser)
echo.

echo The servers are running in separate windows.
echo To stop: Close the terminal windows or press Ctrl+C in each window
echo.

:: Wait and open browser
echo Waiting 5 seconds before opening browser...
timeout /t 5 /nobreak >nul

echo Opening application in browser...
start http://localhost:3000

echo.
echo ================================================================================
echo READY TO USE!
echo ================================================================================
echo.

echo Quick Links:
echo   Dashboard: http://localhost:3000/
echo   Upload Resume: http://localhost:3000/upload
echo   Jobs: http://localhost:3000/jobs
echo   Match Results: http://localhost:3000/match
echo   Analytics: http://localhost:3000/analytics
echo   Evaluation: http://localhost:3000/evaluation
echo.

echo Keep this window open to see server status.
echo Check the other windows for server logs.
echo.

pause
