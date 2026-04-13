@echo off
echo ================================================================================
echo FIXING LXML IMPORT ERROR
echo ================================================================================
echo.

set PYTHON_CMD=
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :fix_start
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :fix_start
)

echo [ERROR] Python not found!
pause
exit /b 1

:fix_start
echo Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo This will fix the lxml import error by:
echo   1. Uninstalling corrupted lxml
echo   2. Uninstalling python-docx
echo   3. Installing lxml 4.9.3 (stable version)
echo   4. Reinstalling python-docx 0.8.11
echo.

set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled
    exit /b 0
)

echo.
echo Step 1: Uninstalling lxml...
%PYTHON_CMD% -m pip uninstall lxml -y

echo.
echo Step 2: Uninstalling python-docx...
%PYTHON_CMD% -m pip uninstall python-docx -y

echo.
echo Step 3: Installing lxml 4.9.3...
%PYTHON_CMD% -m pip install lxml==4.9.3

echo.
echo Step 4: Installing python-docx 0.8.11...
%PYTHON_CMD% -m pip install python-docx==0.8.11

echo.
echo ================================================================================
echo FIX COMPLETE!
echo ================================================================================
echo.

echo Testing import...
%PYTHON_CMD% -c "from lxml import etree; from docx import Document; print('SUCCESS')" 2>&1 | find "SUCCESS" >nul

if %errorlevel% equ 0 (
    echo [OK] lxml and python-docx are now working!
    echo.
    echo You can now run:
    echo   RUN_SERVERS.bat
    echo   RUN_COMPLETE.bat
) else (
    echo [ERROR] Import still failing
    echo.
    echo Try manual installation:
    echo   py -m pip install --upgrade pip
    echo   py -m pip install lxml==4.9.3 --force-reinstall
    echo   py -m pip install python-docx==0.8.11 --force-reinstall
)

echo.
pause
