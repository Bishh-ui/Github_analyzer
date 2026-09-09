@echo off
cls
echo ============================================================
echo   GitHub Analytics Pro - Starting Local Server
echo ============================================================
echo.

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your GitHub token
    echo.
    pause
    exit /b 1
)

REM Check if token is configured
findstr /C:"your_github_token_here" .env >nul
if %ERRORLEVEL% == 0 (
    echo.
    echo ============================================================
    echo   WARNING: GitHub Token Not Configured
    echo ============================================================
    echo.
    echo Please add your GitHub token to the .env file:
    echo 1. Get token from: https://github.com/settings/tokens
    echo 2. Edit .env file
    echo 3. Replace 'your_github_token_here' with your actual token
    echo.
    echo Continuing anyway (limited functionality)...
    echo.
    timeout /t 3 >nul
)

echo Starting server...
echo.
echo Once started, open your browser to:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python run.py

pause
