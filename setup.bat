@echo off
REM Mental Health Symptom Triage - Startup Script for Windows

echo ==========================================
echo Mental Health Symptom Triage - Setup
echo ==========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo X Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo [OK] Node.js found: %NODE_VERSION%
echo.

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo X npm is not installed
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
echo [OK] npm found: %NPM_VERSION%
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
echo.

call npm run install-all

if %ERRORLEVEL% neq 0 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed successfully!
echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the application, run:
echo.
echo   Option 1 (Separate Command Prompts):
echo     Prompt 1: npm run dev
echo     Prompt 2: npm run client
echo.
echo   Option 2 (Combined):
echo     npm run dev:full
echo.
echo Then open: http://localhost:3000
echo.
echo For more details, see QUICKSTART.md
echo ==========================================
echo.
pause
