@echo off
echo ===================================================
echo Starting Dark Web Threat Intelligence Dashboard...
echo ===================================================
cd /d "%~dp0"
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found in .venv
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
streamlit run dashboard.py
pause

