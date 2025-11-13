#!/usr/bin/env python3
"""
Wafid Booking System - Quick Start Guide
Author: MiniMax Agent

Interactive guide to help users set up and use the automation system.
"""

import json
import os
import subprocess
import sys
from colorama import init, Fore, Style

init()  # Initialize colorama

class QuickStart:
    def __init__(self):
        self.config_file = "config.json"
        
    def print_header(self):
        """Print the welcome header."""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}  🏥 WAFID MEDICAL APPOINTMENT AUTOMATION")
        print(f"{Fore.CYAN}         Quick Start Guide")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print()
    
    def check_setup(self):
        """Check if the system is properly set up."""
        print(f"{Fore.YELLOW}📋 Checking System Setup...{Style.RESET_ALL}")
        
        issues = []
        
        # Check Python
        try:
            python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
            print(f"✅ {python_version}")
        except:
            issues.append("Python not found")
        
        # Check required files
        required_files = [
            "wafid_booking_automation.py",
            "monitor_dashboard.py",
            "config.json",
            "requirements.txt"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file}")
            else:
                issues.append(f"Missing file: {file}")
                print(f"❌ {file}")
        
        # Check virtual environment
        if os.path.exists("wafid_booking_env"):
            print(f"✅ Virtual environment")
        else:
            issues.append("Virtual environment not found")
            print(f"❌ Virtual environment")
        
        # Check Chrome/Chromium
        try:
            result = subprocess.run(["google-chrome", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Google Chrome")
            else:
                issues.append("Google Chrome not found")
                print(f"❌ Google Chrome")
        except:
            try:
                result = subprocess.run(["chromium-browser", "--version"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Chromium Browser")
                else:
                    issues.append("Chrome/Chromium not found")
                    print(f"❌ Chrome/Chromium")
            except:
                issues.append("Chrome/Chromium not found")
                print(f"❌ Chrome/Chromium")
        
        print()
        
        if issues:
            print(f"{Fore.RED}❌ Setup Issues Found:{Style.RESET_ALL}")
            for issue in issues:
                print(f"  • {issue}")
            print()
            print(f"{Fore.YELLOW}💡 Run setup.sh (Linux/Mac) or setup.bat (Windows) to fix these issues{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.GREEN}✅ System setup looks good!{Style.RESET_ALL}")
            return True
    
    def configure_system(self):
        """Help user configure the system."""
        print(f"{Fore.YELLOW}⚙️  Configuration Setup{Style.RESET_ALL}")
        print()
        
        # Load existing config
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except:
            print(f"❌ Could not load {self.config_file}")
            return False
        
        print("Please provide your details for booking:")
        print()
        
        # Get user details
        config["user_details"]["full_name"] = input("Full Name: ").strip()
        config["user_details"]["passport_number"] = input("Passport Number: ").strip()
        config["user_details"]["nationality"] = input("Nationality: ").strip()
        config["user_details"]["phone"] = input("Phone Number: ").strip()
        config["user_details"]["email"] = input("Email Address: ").strip()
        
        print()
        print("Booking preferences:")
        config["booking_preferences"]["country"] = input("Country (e.g., Pakistan): ").strip()
        config["booking_preferences"]["city"] = input("City (e.g., Lahore): ").strip()
        config["booking_preferences"]["traveling_country"] = input("Traveling to (e.g., Saudi Arabia): ").strip()
        
        print()
        print("Preferred Medical Centers:")
        print("(You can discover center names using: python3 center_discovery.py --city YourCity --country YourCountry)")
        center1 = input("Preferred Center 1: ").strip()
        center2 = input("Preferred Center 2: ").strip()
        
        if center1:
            config["booking_preferences"]["preferred_centers"] = [center1]
            if center2:
                config["booking_preferences"]["preferred_centers"].append(center2)
        
        # Save configuration
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print()
            print(f"{Fore.GREEN}✅ Configuration saved successfully!{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to save configuration: {e}{Style.RESET_ALL}")
            return False
    
    def show_usage_options(self):
        """Show different ways to use the system."""
        print(f"{Fore.YELLOW}🚀 Usage Options{Style.RESET_ALL}")
        print()
        
        print("1. 🔄 Basic Automation:")
        print("   python3 wafid_booking_automation.py")
        print("   (Runs continuously until appointments are booked)")
        print()
        
        print("2. 📊 With Monitoring Dashboard:")
        print("   Terminal 1: python3 wafid_booking_automation.py")
        print("   Terminal 2: python3 monitor_dashboard.py")
        print("   (Shows real-time progress and statistics)")
        print()
        
        print("3. 🕐 Scheduled Automation:")
        print("   python3 scheduler.py --mode smart")
        print("   (Runs at optimal times throughout the day)")
        print()
        
        print("4. 🔍 Discover Medical Centers:")
        print("   python3 center_discovery.py --city Lahore --country Pakistan")
        print("   (Find exact center names for your area)")
        print()
        
        print("5. ⚙️  Custom Scheduling:")
        print("   python3 scheduler.py --mode custom --start-time 09:00 --end-time 17:00 --interval 60")
        print("   (Custom time range and intervals)")
        print()
    
    def run_discovery_helper(self):
        """Help user discover medical centers."""
        print(f"{Fore.YELLOW}🔍 Medical Center Discovery{Style.RESET_ALL}")
        print()
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            city = config.get("booking_preferences", {}).get("city", "")
            country = config.get("booking_preferences", {}).get("country", "")
            
            if city and country:
                print(f"Running discovery for {city}, {country}...")
                cmd = f"python3 center_discovery.py --city \"{city}\" --country \"{country}\""
                os.system(cmd)
            else:
                print("❌ City and country not configured. Please run configuration first.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def start_automation(self):
        """Start the booking automation."""
        print(f"{Fore.YELLOW}🚀 Starting Automation{Style.RESET_ALL}")
        print()
        
        choice = input("Start with monitoring dashboard? (y/n): ").lower().strip()
        
        if choice == 'y':
            print("Starting automation with monitoring...")
            print()
            print("📋 Instructions:")
            print("1. The booking automation will start in this terminal")
            print("2. Open another terminal and run: python3 monitor_dashboard.py")
            print("3. Use Ctrl+C to stop the automation")
            print()
            input("Press Enter to continue...")
            
            try:
                subprocess.run(["python3", "wafid_booking_automation.py"])
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Automation stopped by user{Style.RESET_ALL}")
        else:
            print("Starting basic automation...")
            try:
                subprocess.run(["python3", "wafid_booking_automation.py"])
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Automation stopped by user{Style.RESET_ALL}")
    
    def main_menu(self):
        """Show the main menu and handle user choices."""
        while True:
            self.print_header()
            
            print("Choose an option:")
            print()
            print("1. 📋 Check System Setup")
            print("2. ⚙️  Configure System")
            print("3. 🔍 Discover Medical Centers")
            print("4. 📖 Show Usage Options")
            print("5. 🚀 Start Automation")
            print("6. ❌ Exit")
            print()
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                print()
                self.check_setup()
                input("\nPress Enter to continue...")
                
            elif choice == "2":
                print()
                self.configure_system()
                input("\nPress Enter to continue...")
                
            elif choice == "3":
                print()
                self.run_discovery_helper()
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                print()
                self.show_usage_options()
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                print()
                if self.check_setup():
                    self.start_automation()
                else:
                    print("❌ Please fix setup issues first")
                input("\nPress Enter to continue...")
                
            elif choice == "6":
                print()
                print("👋 Thank you for using Wafid Booking Automation!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                input("\nPress Enter to continue...")


def main():
    guide = QuickStart()
    guide.main_menu()


if __name__ == "__main__":
    main()