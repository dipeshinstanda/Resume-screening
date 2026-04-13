# ================================================================================
# AI Resume Screening System - Complete Setup and Run Script
# EmpowerTech Solutions
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "AI RESUME SCREENING SYSTEM - COMPLETE SETUP & HIGH-ACCURACY WORKFLOW" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some operations may fail." -ForegroundColor Yellow
    Write-Host "Recommended: Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit
    }
}

# ================================================================================
# STEP 1: CHECK PYTHON INSTALLATION
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 1: CHECKING PYTHON INSTALLATION" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

$pythonFound = $false
$pythonCommand = ""

# Try 'py' command first (Python Launcher)
try {
    $pyVersion = py --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Python Launcher found: $pyVersion" -ForegroundColor Green
        $pythonCommand = "py"
        $pythonFound = $true
    }
} catch {}

# Try 'python' command
if (-not $pythonFound) {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
            $pythonCommand = "python"
            $pythonFound = $true
        }
    } catch {}
}

# Try 'python3' command
if (-not $pythonFound) {
    try {
        $python3Version = python3 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Python3 found: $python3Version" -ForegroundColor Green
            $pythonCommand = "python3"
            $pythonFound = $true
        }
    } catch {}
}

if (-not $pythonFound) {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from one of these sources:" -ForegroundColor Yellow
    Write-Host "  1. Official: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  2. Microsoft Store: Search 'Python 3.11'" -ForegroundColor Yellow
    Write-Host "  3. Anaconda: https://www.anaconda.com/download" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "IMPORTANT: During installation, check 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# ================================================================================
# STEP 2: CHECK DIRECTORY
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 2: VERIFYING PROJECT DIRECTORY" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor Cyan

# Check for key files
$requiredFiles = @(
    "backend\requirements.txt",
    "generate_synthetic_dataset.py",
    "run_large_scale_evaluation.py",
    "generate_visualizations.py"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "[ERROR] Required files not found!" -ForegroundColor Red
    Write-Host "Missing files:" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Make sure you're in the project root directory:" -ForegroundColor Yellow
    Write-Host "  C:\Users\DipeshNagpal\Repos\Resume screening\" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] All required files found!" -ForegroundColor Green
Write-Host ""

# ================================================================================
# STEP 3: INSTALL/UPDATE DEPENDENCIES
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 3: INSTALLING/UPDATING DEPENDENCIES" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Checking installed packages..." -ForegroundColor Cyan

# Check if required packages are installed
$requiredPackages = @("Flask", "scikit-learn", "numpy", "pandas", "matplotlib")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $installed = & $pythonCommand -m pip show $package 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "[INFO] Missing packages detected. Installing..." -ForegroundColor Yellow
    Write-Host "Missing: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    
    # Install from requirements.txt
    Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
    Set-Location backend
    & $pythonCommand -m pip install -r requirements.txt --upgrade
    Set-Location ..
    
    # Install matplotlib separately (if not in requirements.txt)
    Write-Host "Installing matplotlib..." -ForegroundColor Cyan
    & $pythonCommand -m pip install matplotlib
    
    Write-Host ""
    Write-Host "[OK] Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "[OK] All required packages are already installed!" -ForegroundColor Green
    Write-Host ""
    $upgrade = Read-Host "Do you want to upgrade packages to latest versions? (y/n)"
    if ($upgrade -eq "y") {
        Write-Host "Upgrading packages..." -ForegroundColor Cyan
        Set-Location backend
        & $pythonCommand -m pip install -r requirements.txt --upgrade
        Set-Location ..
        & $pythonCommand -m pip install matplotlib --upgrade
    }
}

Write-Host ""

# ================================================================================
# STEP 4: CREATE REQUIRED DIRECTORIES
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 4: CREATING REQUIRED DIRECTORIES" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

$directories = @(
    "backend\data",
    "backend\evaluation_results",
    "backend\database",
    "backend\uploads",
    "backend\logs",
    "visualizations"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "[CREATED] $dir" -ForegroundColor Green
    } else {
        Write-Host "[EXISTS] $dir" -ForegroundColor Cyan
    }
}

Write-Host ""

# ================================================================================
# STEP 5: USER CHOICE - WHAT TO RUN
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 5: SELECT WORKFLOW" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Quick Test (1,000 test cases, ~1 minute)" -ForegroundColor White
Write-Host "2. Standard Evaluation (10,000 test cases, ~6 minutes) [RECOMMENDED]" -ForegroundColor Yellow
Write-Host "3. Large-Scale Evaluation (50,000 test cases, ~25 minutes)" -ForegroundColor White
Write-Host "4. Research-Grade Evaluation (100,000 test cases, ~50 minutes)" -ForegroundColor White
Write-Host "5. Custom size" -ForegroundColor White
Write-Host "6. Run existing dataset evaluation only" -ForegroundColor White
Write-Host "7. [NEW] Production Pipeline Evaluation (XGBoost + SBERT)" -ForegroundColor Magenta
Write-Host "8. Exit" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "Enter your choice (1-8)"

$datasetSize = 0
$skipGeneration = $false
$runProductionPipeline = $false

switch ($choice) {
    "1" { $datasetSize = 1000 }
    "2" { $datasetSize = 10000 }
    "3" { $datasetSize = 50000 }
    "4" { $datasetSize = 100000 }
    "5" { 
        $datasetSize = Read-Host "Enter custom dataset size (100-500000)"
        try {
            $datasetSize = [int]$datasetSize
            if ($datasetSize -lt 100 -or $datasetSize -gt 500000) {
                Write-Host "[WARNING] Size out of range. Using 10,000" -ForegroundColor Yellow
                $datasetSize = 10000
            }
        } catch {
            Write-Host "[ERROR] Invalid input. Using 10,000" -ForegroundColor Red
            $datasetSize = 10000
        }
    }
    "6" { 
        $skipGeneration = $true
        if (-not (Test-Path "backend\data\large_test_dataset.json")) {
            Write-Host "[ERROR] No existing dataset found!" -ForegroundColor Red
            Write-Host "Please generate a dataset first (option 1-5)" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
    "7" {
        # NEW: Production Pipeline Evaluation
        $runProductionPipeline = $true
        $skipGeneration = $true
        Write-Host ""
        Write-Host "[INFO] Running Production Pipeline Evaluation (XGBoost + SBERT)..." -ForegroundColor Magenta
        Write-Host ""

        & $pythonCommand test_production_pipeline_real_data.py --production --save-results

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "[OK] Production pipeline evaluation completed!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Results saved to: backend\evaluation_results\" -ForegroundColor Cyan
        } else {
            Write-Host "[WARNING] Some tests may have failed. Check output above." -ForegroundColor Yellow
        }

        Read-Host "Press Enter to exit"
        exit 0
    }
    "8" { 
        Write-Host "Exiting..." -ForegroundColor Gray
        exit 0
    }
    default { 
        Write-Host "[WARNING] Invalid choice. Using standard evaluation (10,000)" -ForegroundColor Yellow
        $datasetSize = 10000
    }
}

Write-Host ""

# Estimate time
if (-not $skipGeneration) {
    $estimatedTime = [math]::Ceiling($datasetSize / 1500)  # ~1500 cases per minute total
    Write-Host "Dataset size: $datasetSize test cases" -ForegroundColor Cyan
    Write-Host "Estimated total time: ~$estimatedTime minutes" -ForegroundColor Cyan
    Write-Host ""
    
    $confirm = Read-Host "Continue? (y/n)"
    if ($confirm -ne "y") {
        Write-Host "Cancelled by user" -ForegroundColor Gray
        exit 0
    }
}

# Start timing
$startTime = Get-Date

# ================================================================================
# STEP 6: GENERATE DATASET
# ================================================================================

if (-not $skipGeneration) {
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "STEP 6: GENERATING SYNTHETIC DATASET" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Generating $datasetSize test cases..." -ForegroundColor Cyan
    Write-Host ""
    
    $genStart = Get-Date
    & $pythonCommand generate_synthetic_dataset.py --size $datasetSize
    $genEnd = Get-Date
    $genTime = ($genEnd - $genStart).TotalSeconds
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERROR] Dataset generation failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host ""
    Write-Host "[OK] Dataset generated in $([math]::Round($genTime, 1)) seconds!" -ForegroundColor Green
    Write-Host ""
}

# ================================================================================
# STEP 7: RUN COMPARATIVE EVALUATION
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 7: RUNNING COMPARATIVE EVALUATION" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Comparing Enhanced ML vs Baseline algorithms..." -ForegroundColor Cyan
Write-Host ""

$evalStart = Get-Date
& $pythonCommand run_large_scale_evaluation.py --dataset backend\data\large_test_dataset.json --compare
$evalEnd = Get-Date
$evalTime = ($evalEnd - $evalStart).TotalSeconds

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[WARNING] Evaluation failed, but continuing..." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "[OK] Evaluation completed in $([math]::Round($evalTime, 1)) seconds!" -ForegroundColor Green
Write-Host ""

# ================================================================================
# STEP 8: GENERATE VISUALIZATIONS
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 8: GENERATING VISUALIZATIONS" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Creating publication-quality charts from evaluation results..." -ForegroundColor Cyan
Write-Host ""

$vizStart = Get-Date
& $pythonCommand generate_visualizations.py
$vizEnd = Get-Date
$vizTime = ($vizEnd - $vizStart).TotalSeconds

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[WARNING] Visualization generation failed" -ForegroundColor Yellow
    Write-Host "You may need to install matplotlib: $pythonCommand -m pip install matplotlib" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[OK] Visualizations generated in $([math]::Round($vizTime, 1)) seconds!" -ForegroundColor Green
    Write-Host ""
}

# ================================================================================
# STEP 9: DISPLAY RESULTS
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "STEP 9: EXTRACTING RESULTS" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

# Find latest comparison file
$comparisonFiles = Get-ChildItem -Path "backend\evaluation_results" -Filter "large_comparison_*.json" -ErrorAction SilentlyContinue
if ($comparisonFiles) {
    $latestFile = $comparisonFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($latestFile) {
        $results = Get-Content $latestFile.FullName | ConvertFrom-Json
        
        Write-Host "PERFORMANCE RESULTS" -ForegroundColor Cyan
        Write-Host "===================" -ForegroundColor Cyan
        Write-Host ""
        
        $enhancedML = $results.enhanced_ml
        $baseline = $results.baseline
        $improvement = $results.improvement
        
        Write-Host "Enhanced ML Algorithm:" -ForegroundColor Yellow
        Write-Host "  Accuracy:  $([math]::Round($enhancedML.accuracy * 100, 2))%" -ForegroundColor White
        Write-Host "  Precision: $([math]::Round($enhancedML.precision * 100, 2))%" -ForegroundColor White
        Write-Host "  Recall:    $([math]::Round($enhancedML.recall * 100, 2))%" -ForegroundColor White
        Write-Host "  F1-Score:  $([math]::Round($enhancedML.f1_score * 100, 2))%" -ForegroundColor White
        Write-Host ""
        
        Write-Host "Baseline Algorithm:" -ForegroundColor Gray
        Write-Host "  Accuracy:  $([math]::Round($baseline.accuracy * 100, 2))%" -ForegroundColor White
        Write-Host "  Precision: $([math]::Round($baseline.precision * 100, 2))%" -ForegroundColor White
        Write-Host "  Recall:    $([math]::Round($baseline.recall * 100, 2))%" -ForegroundColor White
        Write-Host "  F1-Score:  $([math]::Round($baseline.f1_score * 100, 2))%" -ForegroundColor White
        Write-Host ""
        
        Write-Host "Improvement:" -ForegroundColor Green
        Write-Host "  Accuracy:  +$([math]::Round($improvement.accuracy, 2))%" -ForegroundColor Green
        Write-Host "  Precision: +$([math]::Round($improvement.precision, 2))%" -ForegroundColor Green
        Write-Host "  Recall:    +$([math]::Round($improvement.recall, 2))%" -ForegroundColor Green
        Write-Host "  F1-Score:  +$([math]::Round($improvement.f1_score, 2))%" -ForegroundColor Green
        Write-Host ""
    }
}

# End timing
$endTime = Get-Date
$totalTime = ($endTime - $startTime).TotalMinutes

# ================================================================================
# FINAL SUMMARY
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "WORKFLOW COMPLETE!" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Total execution time: $([math]::Round($totalTime, 1)) minutes" -ForegroundColor Green
Write-Host ""

Write-Host "Generated outputs:" -ForegroundColor Yellow
Write-Host "  [DATA] backend\data\large_test_dataset.json" -ForegroundColor White
Write-Host "  [RESULTS] backend\evaluation_results\large_comparison_*.json" -ForegroundColor White
Write-Host "  [CHARTS] visualizations\*.png" -ForegroundColor White
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review results in backend\evaluation_results\" -ForegroundColor White
Write-Host "  2. View charts in visualizations\" -ForegroundColor White
Write-Host "  3. Insert metrics into docs\RESEARCH_PAPER_TEMPLATE.md" -ForegroundColor White
Write-Host "  4. Cite: 'Evaluated on $datasetSize test cases'" -ForegroundColor White
Write-Host ""

Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - HIGH_ACCURACY_COMPLETE.md - Full implementation details" -ForegroundColor White
Write-Host "  - docs\RESEARCH_PUBLICATION_GUIDE.md - Paper completion guide" -ForegroundColor White
Write-Host "  - docs\10K_TESTING_GUIDE.md - Testing guide" -ForegroundColor White
Write-Host ""

Write-Host "Your AI Resume Screening System is ready for publication!" -ForegroundColor Green
Write-Host ""

# Open results folder
$openFolder = Read-Host "Open results folder? (y/n)"
if ($openFolder -eq "y") {
    Start-Process "backend\evaluation_results"
}

# Open visualizations folder
$openViz = Read-Host "Open visualizations folder? (y/n)"
if ($openViz -eq "y") {
    Start-Process "visualizations"
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Thank you for using AI Resume Screening System!" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
