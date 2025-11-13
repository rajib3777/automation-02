#!/bin/bash

# Wafid Booking Automation Setup Script
# Author: MiniMax Agent

echo "🏥 Wafid Medical Appointment Automation Setup"
echo "=============================================="
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv wafid_booking_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source wafid_booking_env/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing required packages..."
pip install -r requirements.txt

# Install webdriver manager
echo "🚗 Installing Chrome WebDriver..."
pip install webdriver-manager

# Download and setup ChromeDriver
python3 -c "
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

print('🔧 Setting up ChromeDriver...')
try:
    ChromeDriverManager().install()
    print('✅ ChromeDriver installed successfully')
except Exception as e:
    print(f'⚠️  ChromeDriver setup warning: {e}')
    print('You may need to install Google Chrome manually')
"

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p results
mkdir -p screenshots

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x wafid_booking_automation.py
chmod +x monitor_dashboard.py

echo
echo "✅ Setup completed successfully!"
echo
echo "📋 Next Steps:"
echo "1. Edit config.json with your personal details"
echo "2. Update your preferred medical centers"
echo "3. Run: python3 wafid_booking_automation.py"
echo "4. In another terminal, run: python3 monitor_dashboard.py"
echo
echo "🚨 Important:"
echo "- Make sure Google Chrome is installed on your system"
echo "- Update the preferred_centers in config.json with your actual center names"
echo "- Test with a small number of attempts first"
echo
echo "📖 For help, check the README.md file"