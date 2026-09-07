@echo off
echo ========================================
echo RuralAI Finance Hub - Quick Start
echo NABARD Hackathon @ GFF 2026
echo ========================================
echo.

echo Starting Backend Server...
echo.
start cmd /k "cd backend && venv\Scripts\activate && py app.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
echo.
start cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
