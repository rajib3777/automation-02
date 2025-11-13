#!/usr/bin/env python3
"""
Wafid Booking Automation - One-Click Deployment
Author: MiniMax Agent
Date: 2025-09-18

This script will automatically set up and launch your Wafid booking system.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

def print_banner():
    print("\n" + "="*60)
    print("🚀 WAFID BOOKING AUTOMATION - DEPLOYMENT")
    print("   Maximizing Your Appointment Success Rate")
    print("="*60 + "\n")

def check_python():
    print("🔍 Checking Python installation...")
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 7):
        print("❌ Error: Python 3.7+ required. You have:", sys.version)
        return False
    print("✅ Python version:", sys.version.split()[0])
    return True

def install_requirements():
    print("\n📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        print("💡 Try running: pip install selenium requests beautifulsoup4 schedule")
        return False

def setup_config():
    print("\n⚙️ Setting up configuration...")
    
    if os.path.exists("advanced_config.json"):
        print("✅ Configuration file found")
        return True
    
    print("📝 Creating configuration file...")
    
    # Interactive setup
    print("\nPlease provide your details:")
    full_name = input("Full Name: ")
    passport = input("Passport Number: ")
    nationality = input("Nationality: ")
    phone = input("Phone Number: ")
    email = input("Email: ")
    country = input("Country: ")
    city = input("City: ")
    traveling_country = input("Traveling to (e.g., Saudi Arabia): ")
    
    print("\nPreferred Medical Centers:")
    center1 = input("First preferred center: ")
    center2 = input("Second preferred center: ")
    
    config = {
        "user_details": {
            "full_name": full_name,
            "passport_number": passport,
            "nationality": nationality,
            "phone": phone,
            "email": email
        },
        "booking_preferences": {
            "country": country,
            "city": city,
            "traveling_country": traveling_country,
            "preferred_centers": [center1, center2]
        },
        "advanced_settings": {
            "max_concurrent_sessions": 3,
            "retry_delay_seconds": 5,
            "max_attempts_per_session": 50,
            "success_target": 2,
            "enable_ai_optimization": True,
            "run_schedule": "continuous"
        }
    }
    
    with open("advanced_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration saved to advanced_config.json")
    return True

def download_chromedriver():
    print("\n🌐 Setting up Chrome WebDriver...")
    
    # Check if chromedriver exists
    if os.path.exists("chromedriver") or os.path.exists("chromedriver.exe"):
        print("✅ ChromeDriver found")
        return True
    
    print("📥 Downloading ChromeDriver...")
    print("💡 Please download ChromeDriver from: https://chromedriver.chromium.org/")
    print("   Place it in this directory and make it executable")
    
    # Wait for user to download
    input("\nPress Enter after downloading ChromeDriver...")
    
    if os.path.exists("chromedriver") or os.path.exists("chromedriver.exe"):
        # Make executable on Unix systems
        if os.name != 'nt':
            os.chmod("chromedriver", 0o755)
        print("✅ ChromeDriver ready")
        return True
    else:
        print("❌ ChromeDriver not found. Please download it manually.")
        return False

def launch_system():
    print("\n🚀 Launching Wafid Booking System...")
    print("\n" + "="*50)
    print("SYSTEM STARTING - Monitor the progress below:")
    print("="*50)
    
    try:
        # Launch the command center
        subprocess.run([sys.executable, "command_center.py"])
    except KeyboardInterrupt:
        print("\n\n⏹️ System stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching system: {e}")
        print("💡 Try running manually: python command_center.py")

def main():
    print_banner()
    
    # Step 1: Check Python
    if not check_python():
        sys.exit(1)
    
    # Step 2: Install requirements
    if not install_requirements():
        print("\n💡 Please install packages manually and run again")
        sys.exit(1)
    
    # Step 3: Setup configuration
    if not setup_config():
        sys.exit(1)
    
    # Step 4: Setup ChromeDriver
    if not download_chromedriver():
        print("\n💡 Please setup ChromeDriver manually and run again")
        sys.exit(1)
    
    # Step 5: Launch
    print("\n🎉 Setup complete! Launching your booking system...")
    time.sleep(2)
    launch_system()

if __name__ == "__main__":
    main()
