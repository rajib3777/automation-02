#!/bin/bash

echo "🚀 Starting Ultra-Powerful Wafid Automation Tool deployment..."

# Update system packages
apt-get update -y

# Install required system dependencies
apt-get install -y \
    wget \
    gnupg2 \
    software-properties-common \
    unzip \
    xvfb \
    x11vnc \
    fluxbox

# Install Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update -y
apt-get install -y google-chrome-stable

# Install ChromeDriver
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
echo "Installing ChromeDriver version: $CHROME_DRIVER_VERSION"
wget -O /tmp/chromedriver.zip "http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip"
unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm /tmp/chromedriver.zip

# Set up virtual display for headless Chrome
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Deployment setup completed!"
echo "🌐 Starting Ultra-Powerful Wafid Automation Tool..."

# Start the application
exec "$@"
