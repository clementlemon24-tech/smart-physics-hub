@echo off
echo ========================================
echo   DEPLOYING SMART PHYSICS HUB TO HEROKU
echo ========================================
echo.

echo Step 1: Checking if Heroku CLI is installed...
heroku --version
if %errorlevel% neq 0 (
    echo ERROR: Heroku CLI not found!
    echo Please install from: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

echo.
echo Step 2: Logging into Heroku...
heroku login

echo.
echo Step 3: Creating Heroku app...
set /p APP_NAME="Enter your app name (e.g., smart-physics-hub-yourname): "
heroku create %APP_NAME%

echo.
echo Step 4: Setting up Git repository...
git init
git add .
git commit -m "Deploy Smart Physics Hub to Heroku"

echo.
echo Step 5: Setting environment variables...
heroku config:set SECRET_KEY=smart-physics-hub-production-key-%RANDOM%
heroku config:set FLASK_ENV=production

echo.
echo Step 6: Deploying to Heroku...
git push heroku main

echo.
echo Step 7: Opening your live app...
heroku open

echo.
echo ========================================
echo   DEPLOYMENT COMPLETE! 
echo   Your Smart Physics Hub is now live at:
echo   https://%APP_NAME%.herokuapp.com
echo ========================================
pause