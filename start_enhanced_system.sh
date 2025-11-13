#!/bin/bash

echo "🚀 ENHANCED BOOKING SYSTEM STARTUP"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install required packages if not installed
echo "📦 Checking dependencies..."
pip install flask flask-socketio selenium undetected-chromedriver requests beautifulsoup4 numpy aiohttp gunicorn eventlet pillow lxml --quiet

# Set environment variable for password
export SYSTEM_PASSWORD="F@padma2041"

echo "✅ Dependencies checked"
echo ""

echo "🎯 LAUNCHING ENHANCED BOOKING SYSTEM"
echo "===================================="
echo ""
echo "Features:"
echo "✅ Real-time slot monitoring"
echo "✅ Automatic booking system" 
echo "✅ Multi-center tracking"
echo "✅ Live statistics"
echo "✅ Secure dashboard"
echo ""
echo "🌐 Dashboard will be available at: http://localhost:9090"
echo "🔐 Password: F@padma2041"
echo ""
echo "Starting system..."
echo ""

# Launch the enhanced system
python3 launch_enhanced_system.py
