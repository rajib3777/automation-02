#!/usr/bin/env python3
"""
Wafid Booking Automation - Interactive Deployment Guide
Author: MiniMax Agent
Date: 2025-09-18

Step-by-step guided deployment for your Wafid booking system.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_step(step_num, title):
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*60}")

def wait_for_user():
    input("\nPress Enter to continue...")

def main():
    print("\n🎯 WAFID BOOKING AUTOMATION - GUIDED SETUP")
    print("   Follow these steps to get your system running\n")
    
    # Step 1: Prerequisites
    print_step(1, "CHECKING PREREQUISITES")
    print("✅ Python 3.7+")
    print("✅ Chrome Browser")
    print("✅ Internet Connection")
    print("\n💡 Make sure you have these installed before continuing.")
    wait_for_user()
    
    # Step 2: Install Dependencies
    print_step(2, "INSTALLING DEPENDENCIES")
    print("📦 Installing required Python packages...")
    print("\nRunning: pip install -r requirements.txt")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All packages installed successfully")
        else:
            print("❌ Installation failed. Please install manually:")
            print("   pip install selenium requests beautifulsoup4 schedule")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    wait_for_user()
    
    # Step 3: ChromeDriver Setup
    print_step(3, "CHROME WEBDRIVER SETUP")
    print("🌐 ChromeDriver is required to automate the browser.")
    print("\nOptions:")
    print("1. Download from: https://chromedriver.chromium.org/")
    print("2. Use webdriver-manager (automatic)")
    print("\n💡 Recommended: Place chromedriver in this folder")
    
    if not (os.path.exists("chromedriver") or os.path.exists("chromedriver.exe")):
        print("\n❌ ChromeDriver not found in current directory")
        print("Please download and place it here, then continue.")
    else:
        print("\n✅ ChromeDriver found")
    
    wait_for_user()
    
    # Step 4: Configuration
    print_step(4, "CONFIGURATION SETUP")
    
    if os.path.exists("advanced_config.json"):
        print("✅ Configuration file already exists")
        edit = input("\nDo you want to edit it? (y/n): ").lower().strip()
        if edit != 'y':
            wait_for_user()
            # Skip to next step
            print_step(5, "SYSTEM LAUNCH")
            print("🚀 Everything is ready! Choose how to run:")
            print("\n1. Command Center (Recommended):")
            print("   python command_center.py")
            print("\n2. Basic Bot:")
            print("   python advanced_wafid_bot.py")
            print("\n3. With Monitor Dashboard:")
            print("   python monitor_dashboard.py")
            
            choice = input("\nChoose option (1-3): ").strip()
            
            if choice == "1":
                print("\n🚀 Launching Command Center...")
                subprocess.run([sys.executable, "command_center.py"])
            elif choice == "2":
                print("\n🚀 Launching Basic Bot...")
                subprocess.run([sys.executable, "advanced_wafid_bot.py"])
            elif choice == "3":
                print("\n📊 Launching Monitor Dashboard...")
                subprocess.run([sys.executable, "monitor_dashboard.py"])
            else:
                print("\n💡 Run manually with: python command_center.py")
            return
    
    # Interactive configuration setup
    print("📝 Let's set up your booking preferences...")
    print("\nEnter your details:")
    
    config = {
        "user_details": {},
        "booking_preferences": {},
        "advanced_settings": {
            "max_concurrent_sessions": 3,
            "retry_delay_seconds": 5,
            "max_attempts_per_session": 50,
            "success_target": 2,
            "enable_ai_optimization": True,
            "run_schedule": "continuous"
        }
    }
    
    # Collect user details
    config["user_details"]["full_name"] = input("Full Name: ")
    config["user_details"]["passport_number"] = input("Passport Number: ")
    config["user_details"]["nationality"] = input("Nationality: ")
    config["user_details"]["phone"] = input("Phone: ")
    config["user_details"]["email"] = input("Email: ")
    
    # Collect preferences
    config["booking_preferences"]["country"] = input("Country: ")
    config["booking_preferences"]["city"] = input("City: ")
    config["booking_preferences"]["traveling_country"] = input("Traveling to: ")
    
    print("\nPreferred Medical Centers (enter 2):")
    center1 = input("First center: ")
    center2 = input("Second center: ")
    config["booking_preferences"]["preferred_centers"] = [center1, center2]
    
    # Save configuration
    with open("advanced_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration saved!")
    wait_for_user()
    
    # Step 5: Launch
    print_step(5, "SYSTEM LAUNCH")
    print("🎉 Setup complete! Your Wafid booking system is ready.")
    print("\n🚀 Choose how to run:")
    print("\n1. Full System (Recommended):")
    print("   python command_center.py")
    print("\n2. Basic Automation:")
    print("   python advanced_wafid_bot.py")
    print("\n3. Monitor Only:")
    print("   python monitor_dashboard.py")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    print("\n🚀 Starting your booking system...")
    
    if choice == "1":
        subprocess.run([sys.executable, "command_center.py"])
    elif choice == "2":
        subprocess.run([sys.executable, "advanced_wafid_bot.py"])
    elif choice == "3":
        subprocess.run([sys.executable, "monitor_dashboard.py"])
    else:
        print("💡 Run manually with: python command_center.py")

if __name__ == "__main__":
    main()
