#!/usr/bin/env python3
"""
Wafid Booking Automation - Web Application Setup Script
======================================================

This script helps you set up and launch your Wafid booking automation web application
with all the proper configurations for the complete booking form.

Author: MiniMax Agent
Date: 2025-09-18
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

def print_banner():
    """Display the application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         🎯 WAFID BOOKING AUTOMATION - WEB SETUP 🎯          ║
    ║                                                              ║
    ║              Complete Form Field Configuration               ║
    ║                   Ready for wafid.com                       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Check if all required dependencies are installed"""
    print("📋 Checking system requirements...")
    
    required_packages = [
        'flask', 'flask-socketio', 'selenium', 
        'requests', 'beautifulsoup4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    print("✅ All requirements satisfied!")
    return True

def setup_configuration():
    """Interactive configuration setup"""
    print("\n⚙️ Setting up your Wafid booking configuration...")
    print("Please provide the following information for automatic form filling:")
    print("(Press Enter to skip optional fields)")
    
    config = {}
    
    # Appointment Information
    print("\n📅 APPOINTMENT INFORMATION")
    print("-" * 30)
    
    # Show available countries
    countries = ["Algeria", "Angola", "Bangladesh", "Burundi", "Cameroon", "Chad", 
                "Egypt", "Ethiopia", "Ghana", "Guatemala", "India", "Indonesia", 
                "Jordan", "Kenya", "Lebanon", "Malawi", "Mali", "Morocco", "Nepal", 
                "Niger", "Nigeria", "Pakistan", "Panama", "Philippines", "Sierra Leone", 
                "Somalia", "Sri Lanka", "Sudan", "Syria", "Tanzania", "Thailand", 
                "Tunisia", "Turkey", "Uganda"]
    
    print("Available countries:")
    for i, country in enumerate(countries, 1):
        print(f"{i:2d}. {country}")
    
    while True:
        country_input = input(f"\nSelect your country (1-{len(countries)}) or type name [Pakistan]: ").strip()
        if not country_input:
            config['COUNTRY'] = "Pakistan"
            break
        elif country_input.isdigit() and 1 <= int(country_input) <= len(countries):
            config['COUNTRY'] = countries[int(country_input) - 1]
            break
        elif country_input in countries:
            config['COUNTRY'] = country_input
            break
        else:
            print("Invalid selection. Please try again.")
    
    # City selection based on country
    city_data = {
        "Pakistan": ["Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Gujranwala", "Peshawar", "Multan", "Islamabad"],
        "India": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Pune"],
        "Bangladesh": ["Dhaka", "Chittagong", "Khulna", "Rajshahi", "Sylhet", "Rangpur", "Comilla"],
        "Philippines": ["Manila", "Quezon City", "Davao", "Cebu City", "Zamboanga", "Antipolo", "Pasig"],
        "Indonesia": ["Jakarta", "Surabaya", "Bandung", "Bekasi", "Medan", "Tangerang", "Depok"],
        "Nigeria": ["Lagos", "Kano", "Ibadan", "Abuja", "Port Harcourt", "Benin City", "Kaduna"],
        "Egypt": ["Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said", "Suez", "Luxor"],
        "Morocco": ["Casablanca", "Rabat", "Fez", "Marrakech", "Agadir", "Tangier", "Meknes"],
        "Turkey": ["Istanbul", "Ankara", "Izmir", "Bursa", "Adana", "Gaziantep", "Konya"],
        "Syria": ["Damascus", "Aleppo", "Homs", "Lattakia", "Hama"]
    }
    
    if config['COUNTRY'] in city_data:
        cities = city_data[config['COUNTRY']]
        print(f"\nAvailable cities in {config['COUNTRY']}:")
        for i, city in enumerate(cities, 1):
            print(f"{i:2d}. {city}")
        
        city_input = input(f"Select city (1-{len(cities)}) or type name [{cities[0]}]: ").strip()
        if not city_input:
            config['CITY'] = cities[0]
        elif city_input.isdigit() and 1 <= int(city_input) <= len(cities):
            config['CITY'] = cities[int(city_input) - 1]
        elif city_input in cities:
            config['CITY'] = city_input
        else:
            config['CITY'] = cities[0]
    else:
        config['CITY'] = input("City: ").strip() or "Main City"
    
    # Travel destination
    destinations = ["Bahrain", "Kuwait", "Oman", "Qatar", "Saudi Arabia", "UAE", "Yemen"]
    print(f"\nGulf countries you can travel to:")
    for i, dest in enumerate(destinations, 1):
        print(f"{i}. {dest}")
    
    dest_input = input("Select destination (1-7) or type name [Kuwait]: ").strip()
    if not dest_input:
        config['COUNTRY_TRAVELING_TO'] = "Kuwait"
    elif dest_input.isdigit() and 1 <= int(dest_input) <= len(destinations):
        config['COUNTRY_TRAVELING_TO'] = destinations[int(dest_input) - 1]
    elif dest_input in destinations:
        config['COUNTRY_TRAVELING_TO'] = dest_input
    else:
        config['COUNTRY_TRAVELING_TO'] = "Kuwait"
    
    # Personal Information
    print("\n👤 PERSONAL INFORMATION")
    print("-" * 25)
    config['FIRST_NAME'] = input("First Name *: ").strip()
    config['LAST_NAME'] = input("Last Name *: ").strip()
    config['DATE_OF_BIRTH'] = input("Date of Birth (YYYY-MM-DD) *: ").strip()
    
    # Auto-set nationality based on country
    nationality_map = {
        "Algeria": "Algerian", "Angola": "Angolan", "Bangladesh": "Bangladeshi",
        "Burundi": "Burundian", "Cameroon": "Cameroonian", "Chad": "Chadian",
        "Egypt": "Egyptian", "Ethiopia": "Ethiopian", "Ghana": "Ghanaian",
        "Guatemala": "Guatemalan", "India": "Indian", "Indonesia": "Indonesian",
        "Jordan": "Jordanian", "Kenya": "Kenyan", "Lebanon": "Lebanese",
        "Malawi": "Malawian", "Mali": "Malian", "Morocco": "Moroccan",
        "Nepal": "Nepalese", "Niger": "Nigerien", "Nigeria": "Nigerian",
        "Pakistan": "Pakistani", "Panama": "Panamanian", "Philippines": "Filipino",
        "Sierra Leone": "Sierra Leonean", "Somalia": "Somali", "Sri Lanka": "Sri Lankan",
        "Sudan": "Sudanese", "Syria": "Syrian", "Tanzania": "Tanzanian",
        "Thailand": "Thai", "Tunisia": "Tunisian", "Turkey": "Turkish", "Uganda": "Ugandan"
    }
    
    suggested_nationality = nationality_map.get(config['COUNTRY'], config['COUNTRY'])
    config['NATIONALITY'] = input(f"Nationality [{suggested_nationality}]: ").strip() or suggested_nationality
    config['GENDER'] = input("Gender (Male/Female) [Male]: ").strip() or "Male"
    config['MARITAL_STATUS'] = input("Marital Status (Single/Married/Divorced/Widowed) [Single]: ").strip() or "Single"
    
    # Passport Information
    print("\n📖 PASSPORT INFORMATION")
    print("-" * 23)
    config['PASSPORT_NUMBER'] = input("Passport Number *: ").strip()
    config['CONFIRM_PASSPORT_NUMBER'] = config['PASSPORT_NUMBER']  # Auto-fill confirmation
    config['PASSPORT_ISSUE_DATE'] = input("Passport Issue Date (YYYY-MM-DD) *: ").strip()
    config['PASSPORT_ISSUE_PLACE'] = input("Passport Issue Place *: ").strip()
    config['PASSPORT_EXPIRATION_DATE'] = input("Passport Expiration Date (YYYY-MM-DD) *: ").strip()
    config['VISA_TYPE'] = input("Visa Type (Work Visa/Family Visa/etc.) [Work Visa]: ").strip() or "Work Visa"
    
    # Contact Information
    print("\n📞 CONTACT & WORK INFORMATION")
    print("-" * 32)
    config['EMAIL_ADDRESS'] = input("Email Address *: ").strip()
    config['PHONE_NUMBER'] = input("Phone Number *: ").strip()
    config['NATIONAL_ID'] = input("National/Civil ID: ").strip()
    config['POSITION_APPLIED_FOR'] = input("Position Applied For: ").strip()
    
    # Booking Preferences
    print("\n🎯 BOOKING PREFERENCES")
    print("-" * 22)
    config['PREFERRED_CENTER_NAME'] = "Check Up Diagnostic Centre"
    config['PREFERRED_CENTER_CODE'] = "346"
    print(f"Primary Center: {config['PREFERRED_CENTER_NAME']} (Code: {config['PREFERRED_CENTER_CODE']})")
    
    # Automation Settings
    config['MAX_ATTEMPTS'] = input("Max Attempts per Session [100]: ").strip() or "100"
    config['CONCURRENT_SESSIONS'] = input("Concurrent Sessions [3]: ").strip() or "3"
    config['HEADLESS_MODE'] = "True"
    config['AUTO_SUBMIT'] = "False"
    
    # Server Settings
    config['HOST'] = "0.0.0.0"
    config['PORT'] = "5000"
    config['FLASK_ENV'] = "production"
    config['SECRET_KEY'] = "wafid-booking-secret-key-2025"
    
    return config

def save_configuration(config):
    """Save configuration to .env file"""
    print("\n💾 Saving configuration...")
    
    env_content = "# Wafid Booking Automation - Complete Configuration\n"
    env_content += "# " + "=" * 54 + "\n\n"
    
    # Group configurations
    sections = {
        "Flask Application Settings": ['FLASK_ENV', 'SECRET_KEY', 'HOST', 'PORT'],
        "Appointment Information": ['COUNTRY', 'CITY', 'COUNTRY_TRAVELING_TO'],
        "Personal Information": ['FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'NATIONALITY', 'GENDER', 'MARITAL_STATUS'],
        "Passport Information": ['PASSPORT_NUMBER', 'CONFIRM_PASSPORT_NUMBER', 'PASSPORT_ISSUE_DATE', 'PASSPORT_ISSUE_PLACE', 'PASSPORT_EXPIRATION_DATE', 'VISA_TYPE'],
        "Contact & Work Information": ['EMAIL_ADDRESS', 'PHONE_NUMBER', 'NATIONAL_ID', 'POSITION_APPLIED_FOR'],
        "Booking Preferences": ['PREFERRED_CENTER_NAME', 'PREFERRED_CENTER_CODE', 'MAX_ATTEMPTS', 'CONCURRENT_SESSIONS', 'HEADLESS_MODE', 'AUTO_SUBMIT']
    }
    
    for section_name, keys in sections.items():
        env_content += f"# {section_name}\n"
        env_content += "# " + "=" * len(section_name) + "\n"
        
        for key in keys:
            if key in config:
                env_content += f"{key}={config[key]}\n"
        env_content += "\n"
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Configuration saved to .env file")

def validate_configuration(config):
    """Validate required fields"""
    print("\n🔍 Validating configuration...")
    
    required_fields = [
        'FIRST_NAME', 'LAST_NAME', 'DATE_OF_BIRTH', 'NATIONALITY',
        'PASSPORT_NUMBER', 'PASSPORT_ISSUE_DATE', 'PASSPORT_ISSUE_PLACE', 
        'PASSPORT_EXPIRATION_DATE', 'EMAIL_ADDRESS', 'PHONE_NUMBER'
    ]
    
    missing_fields = []
    for field in required_fields:
        if not config.get(field, '').strip():
            missing_fields.append(field)
    
    if missing_fields:
        print("❌ Missing required fields:")
        for field in missing_fields:
            print(f"   - {field}")
        return False
    
    print("✅ All required fields provided!")
    return True

def launch_application():
    """Launch the Flask web application"""
    print("\n🚀 Launching Wafid Booking Automation Web Application...")
    print("\n" + "=" * 60)
    print("📱 ACCESS YOUR DASHBOARD:")
    print("   Local:    http://localhost:5000")
    print("   Network:  http://<your-ip>:5000")
    print("\n⚡ FEATURES READY:")
    print("   ✅ Complete form auto-filling")
    print("   ✅ Real-time booking attempts")
    print("   ✅ Center targeting (Code: 346)")
    print("   ✅ Multi-session support")
    print("   ✅ Live statistics dashboard")
    print("=" * 60)
    print("\n🎯 Starting Flask server...")
    
    try:
        # Import and run the Flask app
        os.environ['PYTHONPATH'] = os.getcwd()
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n⏹️  Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

def main():
    """Main setup routine"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed. Please install missing packages manually.")
        return
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("\n⚠️  Configuration file already exists. Reconfigure? (y/n): ")
        if response.lower() != 'y':
            print("Using existing configuration...")
            launch_application()
            return
    
    # Setup configuration
    config = setup_configuration()
    
    # Validate configuration
    if not validate_configuration(config):
        print("❌ Configuration validation failed. Please run setup again.")
        return
    
    # Save configuration
    save_configuration(config)
    
    # Success message
    print("\n" + "🎉 " + "=" * 56 + " 🎉")
    print("    WAFID BOOKING AUTOMATION SETUP COMPLETE!")
    print("=" * 60)
    print("\n📋 SETUP SUMMARY:")
    print(f"   ✅ User: {config['FIRST_NAME']} {config['LAST_NAME']}")
    print(f"   ✅ Passport: {config['PASSPORT_NUMBER']}")
    print(f"   ✅ Target Center: {config['PREFERRED_CENTER_NAME']} (Code: {config['PREFERRED_CENTER_CODE']})")
    print(f"   ✅ Max Sessions: {config['CONCURRENT_SESSIONS']}")
    
    # Launch application
    input("\nPress Enter to launch the web application...")
    launch_application()

if __name__ == "__main__":
    main()
