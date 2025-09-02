@echo off
echo Starting UAE Legal GraphRAG Backend...
echo.

cd backend
call ..\.venv\Scripts\activate.bat
echo Virtual environment activated.

echo Starting backend server...
python start.py --backend-only

pause
