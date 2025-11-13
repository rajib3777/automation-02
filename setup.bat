@echo off
REM Wafid Booking Automation Setup Script for Windows
REM Author: MiniMax Agent

echo 🏥 Wafid Medical Appointment Automation Setup
echo ==============================================
echo.

REM Check if Python 3 is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 is not installed. Please install Python 3.8 or later.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv wafid_booking_env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call wafid_booking_env\Scripts\activate.bat

REM Upgrade pip
echo 🔧 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📦 Installing required packages...
pip install -r requirements.txt

REM Install webdriver manager
echo 🚗 Installing Chrome WebDriver...
pip install webdriver-manager

REM Download and setup ChromeDriver
echo 🔧 Setting up ChromeDriver...
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install(); print('✅ ChromeDriver installed successfully')"

REM Create directories
echo 📁 Creating directories...
if not exist logs mkdir logs
if not exist results mkdir results
if not exist screenshots mkdir screenshots

echo.
echo ✅ Setup completed successfully!
echo.
echo 📋 Next Steps:
echo 1. Edit config.json with your personal details
echo 2. Update your preferred medical centers
echo 3. Run: python wafid_booking_automation.py
echo 4. In another command prompt, run: python monitor_dashboard.py
echo.
echo 🚨 Important:
echo - Make sure Google Chrome is installed on your system
echo - Update the preferred_centers in config.json with your actual center names
echo - Test with a small number of attempts first
echo.
echo 📖 For help, check the README.md file
echo.
pause