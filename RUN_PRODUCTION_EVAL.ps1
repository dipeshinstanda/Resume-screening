# ================================================================================
# AI Resume Screening System - Production Pipeline Evaluation
# Uses: XGBoost, SBERT Embeddings, Enhanced Features
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "AI RESUME SCREENING SYSTEM - PRODUCTION PIPELINE EVALUATION" -ForegroundColor Cyan
Write-Host "XGBoost + SBERT + Enhanced Features" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# ================================================================================
# CHECK PYTHON
# ================================================================================

$pythonCmd = ""
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Python found: $pythonCmd" -ForegroundColor Green
Write-Host ""

# ================================================================================
# CHECK DEPENDENCIES
# ================================================================================

Write-Host "Checking production dependencies..." -ForegroundColor Cyan

$requiredPackages = @("xgboost", "lightgbm", "sentence-transformers", "shap")
$missingPackages = @()

foreach ($pkg in $requiredPackages) {
    $result = & $pythonCmd -c "import $($pkg.Replace('-','_').Replace('sentence_transformers','sentence_transformers'))" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $pkg
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "[INFO] Installing missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    foreach ($pkg in $missingPackages) {
        & $pythonCmd -m pip install $pkg -q
    }
    Write-Host "[OK] Packages installed" -ForegroundColor Green
} else {
    Write-Host "[OK] All production packages available" -ForegroundColor Green
}

Write-Host ""

# ================================================================================
# SELECT EVALUATION MODE
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "SELECT EVALUATION MODE" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "1. Quick Test (basic tests only)" -ForegroundColor White
Write-Host "2. Standard Evaluation (all 26 tests)" -ForegroundColor Yellow
Write-Host "3. Production Tests Only (tests 20-26)" -ForegroundColor White
Write-Host "4. Full Production Workflow (train + evaluate + save results)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

Write-Host ""

# ================================================================================
# RUN EVALUATION
# ================================================================================

$startTime = Get-Date

switch ($choice) {
    "1" {
        Write-Host "Running quick test..." -ForegroundColor Cyan
        & $pythonCmd test_production_pipeline_real_data.py
    }
    "2" {
        Write-Host "Running standard evaluation (all 26 tests)..." -ForegroundColor Cyan
        & $pythonCmd test_production_pipeline_real_data.py --advanced
    }
    "3" {
        Write-Host "Running production tests only..." -ForegroundColor Cyan
        & $pythonCmd test_production_pipeline_real_data.py --production
    }
    "4" {
        Write-Host "Running full production workflow..." -ForegroundColor Cyan
        Write-Host ""
        
        # Create results directory
        $resultsDir = "backend\evaluation_results"
        if (-not (Test-Path $resultsDir)) {
            New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null
        }
        
        # Run full evaluation with output
        & $pythonCmd test_production_pipeline_real_data.py --production --save-results
        
        Write-Host ""
        Write-Host "[OK] Results saved to: $resultsDir" -ForegroundColor Green
    }
    default {
        Write-Host "Running standard evaluation..." -ForegroundColor Cyan
        & $pythonCmd test_production_pipeline_real_data.py --advanced
    }
}

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "EVALUATION COMPLETE" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Duration: $([math]::Round($duration, 1)) seconds" -ForegroundColor Cyan
Write-Host ""

# ================================================================================
# SHOW RESULTS SUMMARY
# ================================================================================

if (Test-Path "backend\evaluation_results") {
    $latestResults = Get-ChildItem -Path "backend\evaluation_results" -Filter "*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestResults) {
        Write-Host "Latest results file: $($latestResults.Name)" -ForegroundColor Cyan
        Write-Host "View results: Get-Content '$($latestResults.FullName)' | ConvertFrom-Json" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review test output above for accuracy/precision/recall" -ForegroundColor White
Write-Host "  2. Update docs\STEP3_DATASET_COMPLETE.md with new metrics" -ForegroundColor White
Write-Host "  3. Run 'python run_large_scale_evaluation.py' for full dataset eval" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
