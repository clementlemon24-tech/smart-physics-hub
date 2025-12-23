@echo off
cls
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🚀 INSTALL RAILWAY CLI + DEPLOY SMART PHYSICS HUB 🚀              ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

echo 📋 CHECKING RAILWAY CLI INSTALLATION...
railway --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Railway CLI is already installed!
    goto deploy
)

echo ❌ Railway CLI not found. Installing now...
echo.

echo 📥 INSTALLING RAILWAY CLI...
echo.
echo 🔧 METHOD 1: Using PowerShell (Recommended)
echo Running: iwr -useb https://railway.app/install.ps1 ^| iex
echo.

powershell -Command "iwr -useb https://railway.app/install.ps1 | iex"
if %errorlevel% neq 0 (
    echo.
    echo ❌ PowerShell installation failed. Trying alternative method...
    echo.
    echo 🔧 METHOD 2: Manual Download
    echo Opening Railway CLI download page...
    start https://docs.railway.app/develop/cli
    echo.
    echo 📋 MANUAL INSTALLATION STEPS:
    echo 1. Download Railway CLI from the opened page
    echo 2. Install the downloaded file
    echo 3. Restart this script
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Railway CLI installed successfully!
echo.

:deploy
echo 🚀 STARTING DEPLOYMENT PROCESS...
echo.

echo 🔐 STEP 1: LOGIN TO RAILWAY...
echo This will open your browser for authentication...
railway login
if %errorlevel% neq 0 (
    echo ❌ Login failed. Please try again.
    pause
    exit /b 1
)

echo.
echo ✅ Login successful!
echo.

echo 📱 STEP 2: CREATING NEW RAILWAY PROJECT...
railway new smart-physics-hub
if %errorlevel% neq 0 (
    echo ❌ Project creation failed. Trying alternative...
    railway new
)

echo.
echo ✅ Project created!
echo.

echo 🔧 STEP 3: SETTING ENVIRONMENT VARIABLES...
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=smart-physics-hub-railway-production-key-%RANDOM%

echo.
echo ✅ Environment variables set!
echo.

echo 🚀 STEP 4: DEPLOYING YOUR SMART PHYSICS HUB...
echo This may take 2-3 minutes while Railway builds your app...
echo.
railway up
if %errorlevel% neq 0 (
    echo ❌ Deployment failed. Checking logs...
    railway logs
    pause
    exit /b 1
)

echo.
echo 🎉 DEPLOYMENT SUCCESSFUL!
echo.

echo 🌐 STEP 5: GETTING YOUR LIVE URL...
echo Your Smart Physics Hub is now live at:
railway domain

echo.
echo 🚀 STEP 6: OPENING YOUR APP...
railway open

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🎉 SMART PHYSICS HUB SUCCESSFULLY DEPLOYED TO RAILWAY! 🎉         ║
echo ║                                                                      ║
echo ║   Your physics learning platform is now live worldwide!             ║
echo ║                                                                      ║
echo ║   Features available 24/7:                                          ║
echo ║   🤖 AI Tutor (Engineer Clement Ekelemchi)                          ║
echo ║   🏫 Interactive Classroom                                           ║
echo ║   🧪 Virtual Laboratory                                              ║
echo ║   📚 Physics Encyclopedia                                            ║
echo ║   🔬 Nanophysics ^& AI Topics                                        ║
echo ║   📝 JAMB/WAEC/NECO Preparation                                      ║
echo ║                                                                      ║
echo ║   Share your live URL with students worldwide! 🌍                   ║
echo ║                                                                      ║
echo ║   Useful Railway Commands:                                           ║
echo ║   - railway logs (view app logs)                                    ║
echo ║   - railway open (open your app)                                    ║
echo ║   - railway status (check app status)                               ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
pause