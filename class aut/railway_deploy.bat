@echo off
cls
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🚀 RAILWAY CLI DEPLOYMENT - SMART PHYSICS HUB 🚀                  ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

echo 📋 CHECKING RAILWAY CLI...
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found in PATH!
    echo.
    echo 📥 Please install Railway CLI:
    echo 1. Go to: https://docs.railway.app/develop/cli
    echo 2. Download and install Railway CLI
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo ✅ Railway CLI found!
echo.

echo 🔐 LOGGING INTO RAILWAY...
echo Opening browser for authentication...
railway login
if %errorlevel% neq 0 (
    echo ❌ Login failed. Please try again.
    pause
    exit /b 1
)

echo.
echo 📱 CREATING NEW RAILWAY PROJECT...
railway new
if %errorlevel% neq 0 (
    echo ❌ Project creation failed.
    pause
    exit /b 1
)

echo.
echo 🔧 SETTING ENVIRONMENT VARIABLES...
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=smart-physics-hub-railway-production-key

echo.
echo 🚀 DEPLOYING TO RAILWAY...
echo This may take 2-3 minutes...
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
echo 🌐 YOUR APP IS LIVE AT:
railway domain
echo.
echo 🚀 OPENING YOUR APP...
railway open

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🎉 SMART PHYSICS HUB DEPLOYED TO RAILWAY! 🎉                      ║
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
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
pause