#!/usr/bin/env python3
"""
Wafid Booking Automation - Quick Setup for Check Up Diagnostic Centre
Author: MiniMax Agent
Date: 2025-09-18

Optimized setup for your specific center (Code: 346).
"""

import os
import json
import sys

def create_optimized_config():
    """Create optimized configuration for Check Up Diagnostic Centre"""
    
    config = {
        "user_details": {
            "full_name": "Your Full Name Here",
            "passport_number": "AB1234567", 
            "nationality": "Pakistani",
            "phone": "+92-300-1234567",
            "email": "your.email@example.com"
        },
        "booking_preferences": {
            "country": "Pakistan",
            "city": "Lahore",
            "traveling_country": "Saudi Arabia",
            "preferred_centers": [
                "Check Up Diagnostic Centre",
                "Al-Shifa Medical Center"
            ],
            "center_codes": {
                "Check Up Diagnostic Centre": "346",
                "Al-Shifa Medical Center": ""
            },
            "primary_target": {
                "name": "Check Up Diagnostic Centre", 
                "code": "346",
                "priority": 1
            }
        },
        "advanced_settings": {
            "max_concurrent_sessions": 3,
            "retry_delay_seconds": 4,
            "max_attempts_per_session": 100,
            "success_target": 2,
            "enable_ai_optimization": True,
            "enable_center_code_targeting": True,
            "run_schedule": "continuous",
            "stealth_mode": True,
            "random_delays": True,
            "user_agent_rotation": True,
            "center_code_priority": True
        },
        "notification_settings": {
            "enable_notifications": True,
            "email_alerts": False,
            "sound_alerts": True,
            "desktop_notifications": True
        },
        "optimization_settings": {
            "target_specific_code": "346",
            "code_based_selection": True,
            "fallback_to_name_matching": True,
            "enhanced_center_detection": True
        }
    }
    
    return config

def setup_for_check_up_centre():
    """Setup system specifically for Check Up Diagnostic Centre"""
    
    print("🎯 SETTING UP FOR CHECK UP DIAGNOSTIC CENTRE")
    print("=" * 50)
    print("Center Code: 346")
    print("Enhanced Targeting: ENABLED")
    print("=" * 50 + "\n")
    
    # Create optimized config
    config = create_optimized_config()
    
    # Get user details
    print("📝 Please provide your details:\n")
    
    config["user_details"]["full_name"] = input("Full Name: ") or config["user_details"]["full_name"]
    config["user_details"]["passport_number"] = input("Passport Number: ") or config["user_details"]["passport_number"]
    config["user_details"]["nationality"] = input("Nationality [Pakistani]: ") or config["user_details"]["nationality"]
    config["user_details"]["phone"] = input("Phone Number: ") or config["user_details"]["phone"]
    config["user_details"]["email"] = input("Email: ") or config["user_details"]["email"]
    
    # Location details
    print("\n📍 Location Details:\n")
    config["booking_preferences"]["country"] = input("Country [Pakistan]: ") or config["booking_preferences"]["country"]
    config["booking_preferences"]["city"] = input("City [Lahore]: ") or config["booking_preferences"]["city"]
    config["booking_preferences"]["traveling_country"] = input("Traveling to [Saudi Arabia]: ") or config["booking_preferences"]["traveling_country"]
    
    # Ask if they want to add a second center
    print("\n🏥 Center Configuration:\n")
    print("✅ Primary: Check Up Diagnostic Centre (Code: 346)")
    
    second_center = input("Add second preferred center [optional]: ").strip()
    if second_center:
        config["booking_preferences"]["preferred_centers"][1] = second_center
        config["booking_preferences"]["center_codes"][second_center] = ""
    
    # Save configuration
    with open("check_up_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration saved as: check_up_config.json")
    
    # Display summary
    print("\n🚀 SETUP COMPLETE!")
    print("=" * 30)
    print(f"Primary Target: Check Up Diagnostic Centre (346)")
    print(f"User: {config['user_details']['full_name']}")
    print(f"Location: {config['booking_preferences']['city']}, {config['booking_preferences']['country']}")
    print(f"Max Sessions: {config['advanced_settings']['max_concurrent_sessions']}")
    print(f"Code Targeting: ENABLED")
    print("=" * 30)
    
    return config

def launch_with_check_up_config():
    """Launch automation with Check Up Diagnostic Centre configuration"""
    
    print("\n🚀 LAUNCHING AUTOMATION FOR CHECK UP DIAGNOSTIC CENTRE")
    print("=" * 55)
    
    # Check if config exists
    if not os.path.exists("check_up_config.json"):
        print("⚠️  Configuration not found. Creating now...")
        setup_for_check_up_centre()
    
    print("\n🎯 Starting targeted automation...")
    print("📍 Primary Target: Check Up Diagnostic Centre (Code: 346)")
    print("⚡ Enhanced code-based targeting ACTIVE")
    print("🔄 Multiple sessions will launch shortly...")
    
    # Import and run the command center with specific config
    try:
        import subprocess
        subprocess.run([sys.executable, "command_center.py", "--config", "check_up_config.json"])
    except Exception as e:
        print(f"❌ Error launching automation: {e}")
        print("💡 Try running manually: python command_center.py")

def main():
    """Main menu for Check Up Diagnostic Centre setup"""
    
    while True:
        print("\n🏥 CHECK UP DIAGNOSTIC CENTRE - BOOKING AUTOMATION")
        print("=" * 55)
        print("Center Code: 346")
        print("=" * 55)
        
        print("\n🎯 QUICK SETUP MENU:")
        print("1. 🚀 Quick Launch (Auto-setup & Start)")
        print("2. ⚙️  Setup Configuration Only") 
        print("3. 📊 Launch with Existing Config")
        print("4. 📋 View Current Configuration")
        print("5. 🔙 Back to Main System")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            config = setup_for_check_up_centre()
            print("\n⏳ Launching in 3 seconds...")
            import time
            time.sleep(3)
            launch_with_check_up_config()
            break
            
        elif choice == "2":
            setup_for_check_up_centre()
            
        elif choice == "3":
            launch_with_check_up_config()
            break
            
        elif choice == "4":
            if os.path.exists("check_up_config.json"):
                with open("check_up_config.json", "r") as f:
                    config = json.load(f)
                
                print("\n📋 CURRENT CONFIGURATION:")
                print("=" * 30)
                print(f"User: {config['user_details']['full_name']}")
                print(f"Primary Center: {config['booking_preferences']['primary_target']['name']}")
                print(f"Center Code: {config['booking_preferences']['primary_target']['code']}")
                print(f"Location: {config['booking_preferences']['city']}")
                print(f"Sessions: {config['advanced_settings']['max_concurrent_sessions']}")
                print("=" * 30)
            else:
                print("\n❌ No configuration file found")
                
        elif choice == "5":
            break
            
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
