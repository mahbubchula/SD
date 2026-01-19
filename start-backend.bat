@echo off
echo ========================================
echo  Advanced Survey Data Generator
echo  Starting Backend Server...
echo ========================================
echo.

cd backend
call venv\Scripts\activate
python -m app.main

pause
