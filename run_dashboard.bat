@echo off
echo ================================================
echo  CORD-19 Research Dashboard Launcher
echo ================================================
echo.
echo Starting Streamlit dashboard...
echo.
echo The dashboard will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server when done.
echo ================================================
echo.

cd /d "%~dp0"
python -m streamlit run streamlit_app.py

pause
