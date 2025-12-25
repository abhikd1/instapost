@echo off
echo ========================================
echo  Instagram Reel Poster - Git Setup
echo ========================================
echo.

REM Check if Git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git not found in PATH!
    echo Please restart your terminal or add Git to PATH manually.
    echo.
    echo Git is usually installed at: C:\Program Files\Git\cmd
    pause
    exit /b 1
)

echo Git found! Version:
git --version
echo.

REM Configure Git (first time setup)
echo Setting up Git configuration...
git config --global user.name "Sumit"
git config --global user.email "sumit@example.com"
echo.

REM Initialize repository
echo Initializing Git repository...
git init
echo.

REM Add all files
echo Adding files to Git...
git add .
echo.

REM Show what will be committed
echo Files ready to commit:
git status --short
echo.

REM Create first commit
echo Creating first commit...
git commit -m "Initial commit: Instagram Reel Auto-Poster with video processing"
echo.

echo ========================================
echo  SUCCESS! Repository initialized!
echo ========================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub.com
echo 2. Run: git remote add origin YOUR_GITHUB_URL
echo 3. Run: git push -u origin main
echo.
pause
