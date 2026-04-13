@echo off
echo ================================================================================
echo HIGH-ACCURACY WORKFLOW - 10K DATASET
echo EmpowerTech Solutions
echo ================================================================================
echo.

REM Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found!
py --version
echo.

REM Check if in correct directory
if not exist "generate_synthetic_dataset.py" (
    echo ERROR: Not in correct directory
    echo Please run this script from: C:\Users\DipeshNagpal\Repos\Resume screening\
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
py -m pip show scikit-learn >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    cd backend
    py -m pip install -r requirements.txt
    cd ..
)

py -m pip show matplotlib >nul 2>&1
if errorlevel 1 (
    echo Installing matplotlib...
    py -m pip install matplotlib
)

echo.
echo ================================================================================
echo STEP 1: GENERATE 10,000 TEST CASES
echo ================================================================================
echo.

py generate_synthetic_dataset.py --size 10000
if errorlevel 1 (
    echo.
    echo ERROR: Dataset generation failed
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo STEP 2: EVALUATE ENHANCED ML ALGORITHM
echo ================================================================================
echo.

py run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --enhanced
if errorlevel 1 (
    echo.
    echo WARNING: Enhanced ML evaluation failed, continuing...
)

echo.
echo ================================================================================
echo STEP 3: COMPARATIVE EVALUATION
echo ================================================================================
echo.

py run_large_scale_evaluation.py --dataset backend/data/large_test_dataset.json --compare
if errorlevel 1 (
    echo.
    echo WARNING: Comparative evaluation failed, continuing...
)

echo.
echo ================================================================================
echo STEP 4: GENERATE VISUALIZATIONS
echo ================================================================================
echo.

py generate_visualizations.py
if errorlevel 1 (
    echo.
    echo WARNING: Visualization generation failed
)

echo.
echo ================================================================================
echo WORKFLOW COMPLETE!
echo ================================================================================
echo.
echo Generated outputs:
echo   - backend\data\large_test_dataset.json (10,000 cases)
echo   - backend\evaluation_results\large_comparison_*.json
echo   - visualizations\*.png
echo.
echo Next steps:
echo   1. Review results in backend\evaluation_results\
echo   2. View charts in visualizations\
echo   3. Insert metrics into docs\RESEARCH_PAPER_TEMPLATE.md
echo.
pause
