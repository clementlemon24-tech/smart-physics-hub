@echo off
cls
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🚀 SMART PHYSICS HUB - INSTANT CLOUD DEPLOYMENT 🚀                ║
echo ║                                                                      ║
echo ║   Your app is running locally and ready for cloud deployment!       ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

echo 📱 YOUR APP IS CURRENTLY RUNNING AT:
echo    ✅ Local: http://localhost:5000
echo    ✅ Network: http://0.0.0.0:5000
echo.

echo 🌍 CHOOSE CLOUD DEPLOYMENT PLATFORM:
echo.
echo [1] 🚀 Railway (Fastest - 2 minutes)
echo [2] 💚 Render (Free forever)
echo [3] 🔵 Heroku (Most popular)
echo [4] 📖 View deployment guide
echo [5] ❌ Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto railway
if "%choice%"=="2" goto render
if "%choice%"=="3" goto heroku
if "%choice%"=="4" goto guide
if "%choice%"=="5" goto exit
goto invalid

:railway
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                    🚀 RAILWAY DEPLOYMENT                             ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo ⚡ FASTEST DEPLOYMENT - 2 MINUTES!
echo.
echo 📋 STEPS:
echo 1. Opening Railway website...
start https://railway.app/new/template
timeout /t 3 >nul
echo    ✅ Railway opened in browser
echo.
echo 2. Sign up with GitHub (free account)
echo 3. Click "Deploy from GitHub repo"
echo 4. Upload your project folder
echo 5. Railway auto-detects Flask app
echo 6. Wait 2-3 minutes
echo 7. YOUR APP IS LIVE WORLDWIDE! 🎉
echo.
echo 🌐 YOUR LIVE URL WILL BE:
echo    https://smart-physics-hub-production.up.railway.app
echo.
echo 📱 ACCESSIBLE FROM:
echo    ✅ Mobile phones worldwide
echo    ✅ Laptops and desktops
echo    ✅ Tablets and any device
echo    ✅ 24/7 availability
echo.
pause
goto end

:render
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                    💚 RENDER DEPLOYMENT                              ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo 💚 FREE FOREVER DEPLOYMENT!
echo.
echo 📋 STEPS:
echo 1. Opening Render website...
start https://render.com/deploy
timeout /t 3 >nul
echo    ✅ Render opened in browser
echo.
echo 2. Connect GitHub account
echo 3. Click "New Web Service"
echo 4. Upload your project files
echo 5. Render auto-deploys
echo 6. Wait 3-5 minutes
echo 7. YOUR APP IS LIVE WORLDWIDE! 🎉
echo.
echo 🌐 YOUR LIVE URL WILL BE:
echo    https://smart-physics-hub.onrender.com
echo.
echo 📱 ACCESSIBLE FROM:
echo    ✅ Mobile phones worldwide
echo    ✅ Laptops and desktops
echo    ✅ Tablets and any device
echo    ✅ 24/7 availability
echo.
pause
goto end

:heroku
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                    🔵 HEROKU DEPLOYMENT                              ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo 🔵 MOST POPULAR PLATFORM!
echo.
echo 📋 STEPS:
echo 1. Opening Heroku website...
start https://heroku.com/deploy
timeout /t 3 >nul
echo    ✅ Heroku opened in browser
echo.
echo 2. Create free account
echo 3. Click "Create new app"
echo 4. Upload your project files
echo 5. Deploy automatically
echo 6. Wait 5 minutes
echo 7. YOUR APP IS LIVE WORLDWIDE! 🎉
echo.
echo 🌐 YOUR LIVE URL WILL BE:
echo    https://smart-physics-hub-yourname.herokuapp.com
echo.
echo 📱 ACCESSIBLE FROM:
echo    ✅ Mobile phones worldwide
echo    ✅ Laptops and desktops
echo    ✅ Tablets and any device
echo    ✅ 24/7 availability
echo.
pause
goto end

:guide
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                    📖 DEPLOYMENT GUIDES                              ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo Opening deployment guides...
if exist "INSTANT_DEPLOY.md" start notepad "INSTANT_DEPLOY.md"
if exist "ONE_CLICK_DEPLOY.html" start "ONE_CLICK_DEPLOY.html"
echo.
echo 📚 Available guides opened:
echo - INSTANT_DEPLOY.md (Quick reference)
echo - ONE_CLICK_DEPLOY.html (Visual guide)
echo.
pause
goto end

:invalid
echo.
echo ❌ Invalid choice. Please select 1-5.
timeout /t 2 >nul
goto start

:exit
echo.
echo 👋 Exiting deployment script.
echo Your app is still running locally at http://localhost:5000
timeout /t 2 >nul
goto end

:end
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║   🎉 SMART PHYSICS HUB DEPLOYMENT READY! 🎉                         ║
echo ║                                                                      ║
echo ║   Your physics learning platform will be live worldwide!            ║
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