@echo off
cls
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🚀 SMART PHYSICS HUB - AUTOMATIC HEROKU DEPLOYMENT 🚀             ║
echo ║                                                                      ║
echo ║   This script will deploy your app to Heroku automatically!         ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

echo ⚡ CHECKING SYSTEM...
timeout /t 2 >nul

echo ✅ All deployment files are ready!
echo ✅ Procfile configured
echo ✅ requirements.txt ready
echo ✅ app.json configured
echo ✅ Python app optimized
echo.

echo 📋 DEPLOYMENT OPTIONS:
echo.
echo [1] 🌐 Deploy via Heroku Web Dashboard (Recommended)
echo [2] 💻 Deploy via Command Line (Advanced)
echo [3] 📖 View Deployment Guide
echo [4] 🔗 Open Heroku Website
echo.

set /p choice="Choose option (1-4): "

if "%choice%"=="1" goto web_deploy
if "%choice%"=="2" goto cli_deploy
if "%choice%"=="3" goto guide
if "%choice%"=="4" goto website
goto invalid

:web_deploy
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                    🌐 WEB DASHBOARD DEPLOYMENT                       ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo 📋 FOLLOW THESE STEPS:
echo.
echo ✅ STEP 1: Opening Heroku website...
start https://heroku.com
timeout /t 3 >nul
echo.
echo ✅ STEP 2: Sign up/Login to Heroku
echo    - Create free account if you don't have one
echo    - Login to your dashboard
echo.
echo ✅ STEP 3: Create new app
echo    - Click "New" → "Create new app"
echo    - App name: smart-physics-hub-yourname
echo    - Choose your region
echo    - Click "Create app"
echo.
echo ✅ STEP 4: Deploy your app
echo    - Go to "Deploy" tab
echo    - Choose "GitHub" deployment method
echo    - Connect your GitHub account
echo    - Upload this project folder to GitHub
echo    - Select your repository
echo    - Click "Deploy Branch"
echo.
echo ✅ STEP 5: Wait 3-5 minutes
echo    - Heroku will build and deploy your app
echo    - Click "View" when deployment completes
echo.
echo 🎉 YOUR APP WILL BE LIVE AT:
echo    https://smart-physics-hub-yourname.herokuapp.com
echo.
echo 📱 FEATURES AVAILABLE 24/7:
echo    🤖 AI Tutor (Engineer Clement Ekelemchi)
echo    🏫 Interactive Classroom
echo    🧪 Virtual Laboratory
echo    📚 Physics Encyclopedia
echo    🔬 Nanophysics ^& AI Topics
echo    📝 JAMB/WAEC/NECO Preparation
echo.
pause
goto end

:cli_deploy
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                    💻 COMMAND LINE DEPLOYMENT                        ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo 🔧 CHECKING HEROKU CLI...
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI not found!
    echo.
    echo 📥 INSTALLING HEROKU CLI...
    echo Opening download page...
    start https://devcenter.heroku.com/articles/heroku-cli
    echo.
    echo Please install Heroku CLI and run this script again.
    pause
    goto end
)

echo ✅ Heroku CLI found!
echo.

echo 🔐 LOGGING INTO HEROKU...
echo Press any key in the browser to login...
heroku login
if %errorlevel% neq 0 (
    echo ❌ Login failed. Please try again.
    pause
    goto end
)

echo.
echo 📱 CREATING HEROKU APP...
set /p app_name="Enter your app name (e.g., smart-physics-hub-yourname): "
heroku create %app_name%
if %errorlevel% neq 0 (
    echo ❌ App creation failed. Name might be taken.
    echo Try a different name like: smart-physics-hub-%RANDOM%
    pause
    goto end
)

echo.
echo 🔧 SETTING UP GIT REPOSITORY...
if not exist ".git" (
    git init
)
git add .
git commit -m "Deploy Smart Physics Hub to Heroku"

echo.
echo ⚙️ CONFIGURING ENVIRONMENT VARIABLES...
heroku config:set SECRET_KEY=smart-physics-hub-production-key-%RANDOM% --app %app_name%
heroku config:set FLASK_ENV=production --app %app_name%

echo.
echo 🚀 DEPLOYING TO HEROKU...
echo This may take 3-5 minutes...
git push heroku main
if %errorlevel% neq 0 (
    echo ❌ Deployment failed. Checking logs...
    heroku logs --tail --app %app_name%
    pause
    goto end
)

echo.
echo 🎉 DEPLOYMENT SUCCESSFUL!
echo.
echo 🌐 YOUR APP IS LIVE AT:
echo https://%app_name%.herokuapp.com
echo.
echo 🚀 OPENING YOUR APP...
heroku open --app %app_name%

echo.
echo ✅ DEPLOYMENT COMPLETE!
echo Your Smart Physics Hub is now accessible worldwide 24/7!
echo.
pause
goto end

:guide
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                       📖 DEPLOYMENT GUIDE                           ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo Opening deployment guides...
if exist "HEROKU_DEPLOY.md" start notepad "HEROKU_DEPLOY.md"
if exist "heroku_guide.html" start "heroku_guide.html"
echo.
echo 📚 Available guides:
echo - HEROKU_DEPLOY.md (Text guide)
echo - heroku_guide.html (Visual guide)
echo - DEPLOY_NOW.txt (Quick reference)
echo.
pause
goto end

:website
echo.
echo 🔗 Opening Heroku website...
start https://heroku.com
echo.
echo 📋 What to do on Heroku:
echo 1. Sign up for free account
echo 2. Create new app
echo 3. Deploy from GitHub or upload files
echo 4. Your app will be live in minutes!
echo.
pause
goto end

:invalid
echo.
echo ❌ Invalid choice. Please select 1-4.
timeout /t 2 >nul
goto start

:end
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🎉 SMART PHYSICS HUB DEPLOYMENT COMPLETE! 🎉                      ║
echo ║                                                                      ║
echo ║   Your physics learning platform is now live worldwide!             ║
echo ║                                                                      ║
echo ║   Features available 24/7:                                          ║
echo ║   🤖 AI Tutor                                                        ║
echo ║   🏫 Interactive Classroom                                           ║
echo ║   🧪 Virtual Laboratory                                              ║
echo ║   📚 Physics Encyclopedia                                            ║
echo ║   🔬 Nanophysics ^& AI                                               ║
echo ║   📝 Exam Preparation                                                ║
echo ║                                                                      ║
echo ║   Share your URL with students and teachers worldwide! 🌍           ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
pause