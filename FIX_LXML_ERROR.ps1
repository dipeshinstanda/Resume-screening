# ================================================================================
# Fix lxml Import Error on Windows
# Quick fix for: ImportError: cannot import name 'etree' from 'lxml'
# ================================================================================

Write-Host "================================================================================" -ForegroundColor Red
Write-Host "FIXING LXML IMPORT ERROR" -ForegroundColor Red
Write-Host "================================================================================" -ForegroundColor Red
Write-Host ""

# Detect Python command
$pythonCmd = ""
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Using Python: $pythonCmd" -ForegroundColor Cyan
& $pythonCmd --version
Write-Host ""

Write-Host "This will fix the lxml import error by:" -ForegroundColor Yellow
Write-Host "  1. Uninstalling corrupted lxml" -ForegroundColor White
Write-Host "  2. Uninstalling python-docx" -ForegroundColor White
Write-Host "  3. Installing lxml 4.9.3 (stable version)" -ForegroundColor White
Write-Host "  4. Reinstalling python-docx 0.8.11" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Cancelled" -ForegroundColor Gray
    exit 0
}

Write-Host ""
Write-Host "Step 1: Uninstalling lxml..." -ForegroundColor Cyan
& $pythonCmd -m pip uninstall lxml -y

Write-Host ""
Write-Host "Step 2: Uninstalling python-docx..." -ForegroundColor Cyan
& $pythonCmd -m pip uninstall python-docx -y

Write-Host ""
Write-Host "Step 3: Installing lxml 4.9.3..." -ForegroundColor Cyan
& $pythonCmd -m pip install lxml==4.9.3

Write-Host ""
Write-Host "Step 4: Installing python-docx 0.8.11..." -ForegroundColor Cyan
& $pythonCmd -m pip install python-docx==0.8.11

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "FIX COMPLETE!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Testing import..." -ForegroundColor Cyan
$testResult = & $pythonCmd -c "from lxml import etree; from docx import Document; print('SUCCESS')" 2>&1

if ($testResult -match "SUCCESS") {
    Write-Host "[OK] lxml and python-docx are now working!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Yellow
    Write-Host "  .\RUN_SERVERS.ps1" -ForegroundColor White
    Write-Host "  .\RUN_COMPLETE.ps1" -ForegroundColor White
} else {
    Write-Host "[ERROR] Import still failing. Error:" -ForegroundColor Red
    Write-Host $testResult -ForegroundColor Red
    Write-Host ""
    Write-Host "Try manual installation:" -ForegroundColor Yellow
    Write-Host "  py -m pip install --upgrade pip" -ForegroundColor White
    Write-Host "  py -m pip install lxml==4.9.3 --force-reinstall" -ForegroundColor White
    Write-Host "  py -m pip install python-docx==0.8.11 --force-reinstall" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"
