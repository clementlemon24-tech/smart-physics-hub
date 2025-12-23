@echo off
echo Starting Pest Tracker Application...
echo.

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "ip=%%a"
    goto :got_ip
)
:got_ip
set ip=%ip: =%

echo ============================================================
echo MOBILE ACCESS:
echo    On your phone, go to: http://%ip%:5000
echo COMPUTER ACCESS:
echo    On this computer: http://localhost:5000
echo ============================================================
echo Make sure your phone is on the same WiFi network!
echo Press Ctrl+C to stop the server
echo ------------------------------------------------------------
echo.

REM Try different Python commands
python run_pest_tracker.py 2>nul && goto :success
py run_pest_tracker.py 2>nul && goto :success
python3 run_pest_tracker.py 2>nul && goto :success
"C:\Users\clementlemon\AppData\Local\Programs\Python\Python38\python.exe" run_pest_tracker.py 2>nul && goto :success

REM If none work, show error message
echo ERROR: Python is not installed or not found in PATH
echo.
echo Please install Python from https://python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation
echo.
pause
goto :end

:success
echo Pest Tracker started successfully!

:end