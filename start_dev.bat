@echo off
echo Starting English to Ijaw Audio Translator...
echo.

echo Setting up backend...
cd backend

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo Generating sample audio files...
python generate_sample_audio.py

echo Starting FastAPI backend...
start "Backend Server" cmd /k "python main.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Setting up frontend...
cd ..\frontend

echo Installing frontend dependencies...
if not exist node_modules (
    npm install
)

echo Starting React frontend...
start "Frontend Server" cmd /k "npm start"

echo.
echo ========================================
echo  English to Ijaw Audio Translator
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Both servers are starting...
echo The frontend will open automatically in your browser.
echo.
echo Press any key to exit...
pause > nul