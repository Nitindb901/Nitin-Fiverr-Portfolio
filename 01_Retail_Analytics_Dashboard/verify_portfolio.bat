@echo off
REM ============================================
REM Portfolio Verification Script
REM Checks all project files before Git push
REM ============================================

echo ============================================
echo Retail Analytics Portfolio - File Checker
echo ============================================
echo.

REM Navigate to project directory
cd /d "C:\Users\nitin\OneDrive\Desktop\Nitin-Fiverr-Portfolio\01_Retail_Analytics_Dashboard"

echo [1/10] Checking project structure...
if exist "data" (echo     ✓ data folder exists) else (echo     ✗ data folder missing & exit /b 1)
if exist "scripts" (echo     ✓ scripts folder exists) else (echo     ✗ scripts folder missing & exit /b 1)
if exist "notebooks" (echo     ✓ notebooks folder exists) else (echo     ✗ notebooks folder missing & exit /b 1)
if exist "dashboard" (echo     ✓ dashboard folder exists) else (echo     ✗ dashboard folder missing & exit /b 1)
if exist "results" (echo     ✓ results folder exists) else (echo     ✗ results folder missing & exit /b 1)
echo.

echo [2/10] Checking Python scripts...
if exist "scripts\generate_data.py" (echo     ✓ generate_data.py found) else (echo     ✗ generate_data.py missing & exit /b 1)
if exist "scripts\etl_clean.py" (echo     ✓ etl_clean.py found) else (echo     ✗ etl_clean.py missing & exit /b 1)
if exist "scripts\export_for_dashboard.py" (echo     ✓ export_for_dashboard.py found) else (echo     ✗ export_for_dashboard.py missing & exit /b 1)
if exist "scripts\generate_visualizations.py" (echo     ✓ generate_visualizations.py found) else (echo     ✗ generate_visualizations.py missing & exit /b 1)
echo.

echo [3/10] Checking data files...
if exist "data\retail_transactions_raw.csv" (echo     ✓ retail_transactions_raw.csv found) else (echo     ✗ retail_transactions_raw.csv missing)
if exist "data\retail_transactions_clean.csv" (echo     ✓ retail_transactions_clean.csv found) else (echo     ✗ retail_transactions_clean.csv missing)
echo.

echo [4/10] Checking dashboard exports...
if exist "dashboard\powerbi_ready.csv" (echo     ✓ powerbi_ready.csv found) else (echo     ✗ powerbi_ready.csv missing)
if exist "dashboard\daily_aggregation.csv" (echo     ✓ daily_aggregation.csv found) else (echo     ✗ daily_aggregation.csv missing)
if exist "dashboard\category_aggregation.csv" (echo     ✓ category_aggregation.csv found) else (echo     ✗ category_aggregation.csv missing)
if exist "dashboard\store_performance.csv" (echo     ✓ store_performance.csv found) else (echo     ✗ store_performance.csv missing)
if exist "dashboard\monthly_trend.csv" (echo     ✓ monthly_trend.csv found) else (echo     ✗ monthly_trend.csv missing)
echo.

echo [5/10] Checking visualizations...
set CHART_COUNT=0
for %%f in (results\*.png) do set /a CHART_COUNT+=1
echo     ✓ Found %CHART_COUNT% visualization files
if %CHART_COUNT% GEQ 10 (echo     ✓ All visualizations present) else (echo     ⚠ Expected 10 visualizations, found %CHART_COUNT%)
echo.

echo [6/10] Checking documentation...
if exist "README.md" (echo     ✓ README.md found) else (echo     ✗ README.md missing & exit /b 1)
if exist "MASTER_PROMPT.md" (echo     ✓ MASTER_PROMPT.md found) else (echo     ✗ MASTER_PROMPT.md missing & exit /b 1)
if exist "dashboard\DATA_DICTIONARY.md" (echo     ✓ DATA_DICTIONARY.md found) else (echo     ✗ DATA_DICTIONARY.md missing)
if exist "dashboard\POWER_BI_SETUP_GUIDE.md" (echo     ✓ POWER_BI_SETUP_GUIDE.md found) else (echo     ✗ POWER_BI_SETUP_GUIDE.md missing)
if exist "dashboard\EXCEL_DASHBOARD_GUIDE.md" (echo     ✓ EXCEL_DASHBOARD_GUIDE.md found) else (echo     ✗ EXCEL_DASHBOARD_GUIDE.md missing)
echo.

echo [7/10] Checking Jupyter notebook...
if exist "notebooks\retail_eda_analysis.ipynb" (echo     ✓ retail_eda_analysis.ipynb found) else (echo     ✗ retail_eda_analysis.ipynb missing)
echo.

echo [8/10] Checking portfolio integration files...
if exist "PORTFOLIO_CARD.html" (echo     ✓ PORTFOLIO_CARD.html found) else (echo     ✗ PORTFOLIO_CARD.html missing)
if exist "PORTFOLIO_INTEGRATION_GUIDE.md" (echo     ✓ PORTFOLIO_INTEGRATION_GUIDE.md found) else (echo     ✗ PORTFOLIO_INTEGRATION_GUIDE.md missing)
echo.

echo [9/10] Checking requirements and config files...
if exist "requirements.txt" (echo     ✓ requirements.txt found) else (echo     ✗ requirements.txt missing & exit /b 1)
if exist ".gitignore" (echo     ✓ .gitignore found) else (echo     ⚠ .gitignore missing - recommended)
echo.

echo [10/10] Checking file sizes...
echo     Checking for files larger than 100MB...
powershell -Command "Get-ChildItem -Recurse -File | Where-Object {$_.Length -gt 100MB} | ForEach-Object { Write-Host '     ⚠ Large file:' $_.Name ([math]::Round($_.Length/1MB,2))'MB' }"
echo     ✓ File size check complete
echo.

REM Check total project size
echo Calculating total project size...
for /f "tokens=3" %%a in ('dir /s /-c ^| find "bytes"') do set SIZE=%%a
set /a SIZE_MB=%SIZE:~0,-6%
echo     Total project size: ~%SIZE_MB% MB
echo.

echo ============================================
echo Verification Complete!
echo ============================================
echo.
echo Your Retail Analytics Dashboard is ready for GitHub!
echo.
echo Next Steps:
echo 1. Install Git from https://git-scm.com/download/win
echo 2. Restart PowerShell/Terminal
echo 3. Run: cd C:\Users\nitin\OneDrive\Desktop\Nitin-Fiverr-Portfolio
echo 4. Run: git init
echo 5. Run: git add .
echo 6. Run: git commit -m "Add Retail Analytics Dashboard project"
echo 7. Create GitHub repo at: https://github.com/new
echo 8. Run: git remote add origin https://github.com/nitindb901/Nitin-Fiverr-Portfolio.git
echo 9. Run: git push -u origin main
echo.
echo Or use GitHub Desktop (easier):
echo 1. Download from: https://desktop.github.com/
echo 2. Add this folder as repository
echo 3. Click "Publish repository"
echo.
echo See GIT_PUSH_INSTRUCTIONS.md for detailed steps!
echo.
pause
