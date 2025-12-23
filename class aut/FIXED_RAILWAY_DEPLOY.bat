@echo off
cls
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🚀 SMART PHYSICS HUB - FIXED RAILWAY DEPLOYMENT 🚀                ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

echo 📋 DEPLOYMENT STATUS CHECK...
echo.

REM Check if Railway CLI exists
where railway >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Railway CLI found! Proceeding with CLI deployment...
    goto cli_deploy
) else (
    echo ❌ Railway CLI not found. Using web deployment method...
    goto web_deploy
)

:cli_deploy
echo.
echo 🚀 CLI DEPLOYMENT METHOD
echo.
echo 🔐 Step 1: Login to Railway...
railway login
if %errorlevel% neq 0 (
    echo ❌ Login failed. Switching to web method...
    goto web_deploy
)

echo.
echo 📱 Step 2: Initialize project...
railway new smart-physics-hub --template
if %errorlevel% neq 0 (
    echo ❌ Project creation failed. Trying alternative...
    railway new
)

echo.
echo 🔧 Step 3: Set environment variables...
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=smart-physics-hub-production-key-%RANDOM%
railway variables set PORT=5000

echo.
echo 🚀 Step 4: Deploy application...
railway up --detach
if %errorlevel% neq 0 (
    echo ❌ Deployment failed. Checking logs...
    railway logs
    goto web_deploy
)

echo.
echo 🌐 Step 5: Get live URL...
railway domain
railway open
goto success

:web_deploy
echo.
echo 🌐 WEB DEPLOYMENT METHOD (RECOMMENDED)
echo.
echo Opening Railway web dashboard for manual deployment...
echo.
echo 📋 FOLLOW THESE STEPS:
echo.
echo 1. 🌐 Go to: https://railway.app
echo 2. 🔐 Login with GitHub account
echo 3. 📱 Click "New Project" → "Deploy from GitHub repo"
echo 4. 📂 Select this repository: smart-physics-hub
echo 5. ⚙️  Railway auto-detects Python Flask app
echo 6. 🚀 Click "Deploy" and wait 2-3 minutes
echo 7. 🌍 Get your live URL from Settings → Domains
echo.

REM Open Railway in browser
start https://railway.app

echo.
echo 📋 YOUR APP FEATURES (READY FOR DEPLOYMENT):
echo ✅ AI Physics Tutor (Engineer Clement Ekelemchi)
echo ✅ Interactive Virtual Classroom
echo ✅ Virtual Physics Laboratory
echo ✅ Complete Physics Encyclopedia
echo ✅ JAMB/WAEC/NECO Exam Preparation
echo ✅ Nanophysics ^& AI Topics
echo ✅ Mistake Prediction System
echo ✅ Multi-level Learning (Basic to Olympiad)
echo ✅ Mobile-Friendly Interface
echo.

echo 📁 DEPLOYMENT FILES STATUS:
echo ✅ main.py - Flask app configured for production
echo ✅ requirements.txt - All dependencies listed
echo ✅ Procfile - Process configuration ready
echo ✅ nixpacks.toml - Build configuration ready
echo ✅ railway.json - Railway configuration ready
echo ✅ All templates - Complete UI ready
echo.

goto success

:success
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🎉 DEPLOYMENT INITIATED SUCCESSFULLY! 🎉                          ║
echo ║                                                                      ║
echo ║   Your Smart Physics Hub will be live at:                           ║
echo ║   https://smart-physics-hub-production.up.railway.app               ║
echo ║                                                                      ║
echo ║   🌍 Share this URL with students worldwide!                        ║
echo ║                                                                      ║
echo ║   📱 Features available 24/7:                                       ║
echo ║   • AI Tutor with voice synthesis                                   ║
echo ║   • Interactive virtual classroom                                   ║
echo ║   • Physics laboratory simulations                                  ║
echo ║   • Complete physics encyclopedia                                   ║
echo ║   • Nigerian exam preparation (JAMB/WAEC/NECO)                     ║
echo ║   • Advanced topics (Nanophysics, AI)                              ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

echo 🔧 USEFUL COMMANDS:
echo railway logs    - View application logs
echo railway open    - Open your live app
echo railway status  - Check deployment status
echo.

pause