@echo off
title Enhanced Booking System Startup

echo 🚀 ENHANCED BOOKING SYSTEM STARTUP
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed
    pause
    exit /b 1
)

REM Install required packages
echo 📦 Checking dependencies...
pip install flask flask-socketio selenium undetected-chromedriver requests beautifulsoup4 numpy aiohttp gunicorn eventlet pillow lxml --quiet

REM Set environment variable for password
set SYSTEM_PASSWORD=F@padma2041

echo ✅ Dependencies checked
echo.

echo 🎯 LAUNCHING ENHANCED BOOKING SYSTEM
echo ====================================
echo.
echo Features:
echo ✅ Real-time slot monitoring
echo ✅ Automatic booking system
echo ✅ Multi-center tracking
echo ✅ Live statistics
echo ✅ Secure dashboard
echo.
echo 🌐 Dashboard will be available at: http://localhost:9090
echo 🔐 Password: F@padma2041
echo.
echo Starting system...
echo.

REM Launch the enhanced system
python launch_enhanced_system.py

pause
