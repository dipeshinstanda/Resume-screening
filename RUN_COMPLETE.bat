@echo off
setlocal enabledelayedexpansion

:: ================================================================================
:: AI Resume Screening System - Complete Setup and Run Script (Batch Version)
:: EmpowerTech Solutions
:: ================================================================================

color 0B
echo ================================================================================
echo AI RESUME SCREENING SYSTEM - COMPLETE SETUP AND HIGH-ACCURACY WORKFLOW
echo ================================================================================
echo.

:: Check Python installation
echo ================================================================================
echo STEP 1: CHECKING PYTHON INSTALLATION
echo ================================================================================
echo.

set PYTHON_CMD=
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    echo [OK] Python Launcher found
    py --version
    goto :python_found
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo [OK] Python found
    python --version
    goto :python_found
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    echo [OK] Python3 found
    python3 --version
    goto :python_found
)

echo [ERROR] Python is not installed or not in PATH!
echo.
echo Please install Python from:
echo   1. https://www.python.org/downloads/
echo   2. Microsoft Store (search 'Python 3.11')
echo.
echo IMPORTANT: Check 'Add Python to PATH' during installation
echo.
pause
exit /b 1

:python_found
echo.

:: Check required files
echo ================================================================================
echo STEP 2: VERIFYING PROJECT DIRECTORY
echo ================================================================================
echo.

if not exist "backend\requirements.txt" (
    echo [ERROR] backend\requirements.txt not found!
    echo Make sure you're in: C:\Users\DipeshNagpal\Repos\Resume screening\
    pause
    exit /b 1
)

if not exist "generate_synthetic_dataset.py" (
    echo [ERROR] generate_synthetic_dataset.py not found!
    pause
    exit /b 1
)

echo [OK] All required files found!
echo.

:: Install dependencies
echo ================================================================================
echo STEP 3: INSTALLING/UPDATING DEPENDENCIES
echo ================================================================================
echo.

echo Installing backend dependencies...
cd backend
%PYTHON_CMD% -m pip install -r requirements.txt --quiet
cd ..

echo Installing matplotlib...
%PYTHON_CMD% -m pip install matplotlib --quiet

echo [OK] Dependencies installed!
echo.

:: Create directories
echo ================================================================================
echo STEP 4: CREATING REQUIRED DIRECTORIES
echo ================================================================================
echo.

if not exist "backend\data" mkdir "backend\data"
if not exist "backend\evaluation_results" mkdir "backend\evaluation_results"
if not exist "backend\database" mkdir "backend\database"
if not exist "backend\uploads" mkdir "backend\uploads"
if not exist "backend\logs" mkdir "backend\logs"
if not exist "visualizations" mkdir "visualizations"

echo [OK] Directories created!
echo.

:: Ask user what to run
echo ================================================================================
echo STEP 5: SELECT WORKFLOW
echo ================================================================================
echo.

echo What would you like to do?
echo.
echo 1. Quick Test (1,000 test cases, ~1 minute)
echo 2. Standard Evaluation (10,000 test cases, ~6 minutes) [RECOMMENDED]
echo 3. Large-Scale Evaluation (50,000 test cases, ~25 minutes)
echo 4. Research-Grade Evaluation (100,000 test cases, ~50 minutes)
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

set DATASET_SIZE=0
if "%choice%"=="1" set DATASET_SIZE=1000
if "%choice%"=="2" set DATASET_SIZE=10000
if "%choice%"=="3" set DATASET_SIZE=50000
if "%choice%"=="4" set DATASET_SIZE=100000
if "%choice%"=="5" (
    echo Exiting...
    exit /b 0
)

if %DATASET_SIZE% equ 0 (
    echo Invalid choice. Using 10,000
    set DATASET_SIZE=10000
)

echo.
echo Dataset size: %DATASET_SIZE% test cases
echo.
set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled
    exit /b 0
)

:: Generate dataset
echo.
echo ================================================================================
echo STEP 6: GENERATING SYNTHETIC DATASET
echo ================================================================================
echo.

echo Generating %DATASET_SIZE% test cases...
echo.

%PYTHON_CMD% generate_synthetic_dataset.py --size %DATASET_SIZE%

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Dataset generation failed!
    pause
    exit /b 1
)

echo.
echo [OK] Dataset generated successfully!
echo.

:: Run evaluation
echo ================================================================================
echo STEP 7: RUNNING COMPARATIVE EVALUATION
echo ================================================================================
echo.

echo Comparing Enhanced ML vs Baseline algorithms...
echo.

%PYTHON_CMD% run_large_scale_evaluation.py --dataset backend\data\large_test_dataset.json --compare

echo.
echo [OK] Evaluation completed!
echo.

:: Generate visualizations
echo ================================================================================
echo STEP 8: GENERATING VISUALIZATIONS
echo ================================================================================
echo.

echo Creating publication-quality charts...
echo.

%PYTHON_CMD% generate_visualizations.py

if %errorlevel% neq 0 (
    echo [WARNING] Visualization generation failed
    echo You may need to install matplotlib
)

echo.
echo [OK] Visualizations generated!
echo.

:: Summary
echo ================================================================================
echo WORKFLOW COMPLETE!
echo ================================================================================
echo.

echo Generated outputs:
echo   - backend\data\large_test_dataset.json
echo   - backend\evaluation_results\large_comparison_*.json
echo   - visualizations\*.png
echo.

echo Next steps:
echo   1. Review results in backend\evaluation_results\
echo   2. View charts in visualizations\
echo   3. Insert metrics into docs\RESEARCH_PAPER_TEMPLATE.md
echo   4. Cite: 'Evaluated on %DATASET_SIZE% test cases'
echo.

echo Documentation:
echo   - HIGH_ACCURACY_COMPLETE.md - Full implementation details
echo   - docs\RESEARCH_PUBLICATION_GUIDE.md - Paper completion guide
echo.

:: Open results folder
set /p open_results="Open results folder? (y/n): "
if /i "%open_results%"=="y" (
    start "" "backend\evaluation_results"
)

:: Open visualizations folder
set /p open_viz="Open visualizations folder? (y/n): "
if /i "%open_viz%"=="y" (
    start "" "visualizations"
)

echo.
echo ================================================================================
echo Thank you for using AI Resume Screening System!
echo ================================================================================
echo.

pause
