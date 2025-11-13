"""
🎯 COMPLETE BOOKING SYSTEM LAUNCHER
===================================
Integrated system with monitoring, auto-booking, and dashboard
"""

import os
import sys
import json
import time
import threading
import subprocess
from datetime import datetime
from flask import Flask
from flask_socketio import SocketIO

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = {
        'flask': 'flask',
        'flask-socketio': 'flask_socketio', 
        'selenium': 'selenium',
        'undetected-chromedriver': 'undetected_chromedriver',
        'requests': 'requests',
        'beautifulsoup4': 'bs4'
    }
    
    missing = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 Install with: pip install " + " ".join(missing))
        return False
    
    print("✅ All dependencies are installed")
    return True

def setup_directories():
    """Create necessary directories"""
    directories = ['templates', 'uploads', 'logs', 'backups']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
    
    print("✅ Directory structure verified")

def verify_configuration():
    """Verify and update configuration file"""
    config_file = 'config.json'
    
    # Default configuration
    default_config = {
        "user_details": {
            "full_name": "Farid Hossain",
            "passport_number": "AE5241562",
            "nationality": "Bangladesh",
            "phone": "+8801234567890",
            "email": "mominit8@gmail.com"
        },
        "booking_preferences": {
            "country": "Pakistan",
            "city": "Lahore",
            "traveling_country": "Saudi Arabia",
            "preferred_centers": [
                "Precision Diagnostics Ltd",
                "Mediquest Diagnostics Ltd", 
                "Allied Diagnostics Ltd",
                "Al-Shifa Medical Center",
                "National Medical Center",
                "Shaukat Khanum Memorial Cancer Hospital",
                "Chughtai Lab",
                "Excel Lab",
                "Dr. Essa's Laboratory"
            ],
            "priority_centers": [
                "Precision Diagnostics Ltd",
                "Mediquest Diagnostics Ltd",
                "Allied Diagnostics Ltd"
            ],
            "monitoring_enabled": True,
            "auto_booking_enabled": True
        },
        "automation_settings": {
            "max_attempts": 500,
            "delay_between_attempts": 30,
            "timeout": 20,
            "headless": False,
            "retry_failed_centers": True,
            "save_screenshots": True,
            "continuous_monitoring": True,
            "monitoring_interval": 60,
            "auto_booking_threshold": 85,
            "max_daily_bookings": 5,
            "priority_booking": True,
            "backup_centers": True,
            "max_workers": 3
        },
        "notification_settings": {
            "email_notifications": True,
            "webhook_url": "",
            "success_sound": True,
            "desktop_notifications": True,
            "sms_alerts": False,
            "booking_confirmation_email": True,
            "slot_detection_alerts": True,
            "monitoring_status_updates": True
        }
    }
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print("✅ Configuration file loaded")
    except FileNotFoundError:
        config = default_config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration file created with defaults")
    
    # Ensure auto-booking is enabled
    config['booking_preferences']['auto_booking_enabled'] = True
    config['booking_preferences']['monitoring_enabled'] = True
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config

def initialize_database():
    """Initialize appointments database if not exists"""
    db_file = 'appointments_database.json'
    
    if not os.path.exists(db_file):
        default_db = {
            "appointments": [
                {
                    "id": 1,
                    "name": "Farid Hossain",
                    "email": "mominit8@gmail.com",
                    "passport_no": "AE5241562",
                    "center": "Precision Diagnostics Ltd",
                    "date": "2025-01-15",
                    "time": "10:30 AM",
                    "amount": 10.0,
                    "status": "Confirmed",
                    "created_at": "2025-09-21T16:04:47.961008",
                    "payment_status": "Completed",
                    "payment_id": "PAY_20250921_3BECA6BF",
                    "payment_confirmed_at": "2025-09-21T16:05:27.148625"
                }
            ]
        }
        
        with open(db_file, 'w') as f:
            json.dump(default_db, f, indent=2)
        
        print("✅ Database initialized with existing appointment")
    else:
        print("✅ Database file exists")

def start_enhanced_dashboard():
    """Start the enhanced dashboard"""
    print("🚀 Starting Enhanced Dashboard...")
    
    try:
        # Import and run the enhanced dashboard
        import enhanced_booking_dashboard
        enhanced_booking_dashboard.socketio.run(
            enhanced_booking_dashboard.app, 
            debug=False, 
            host='0.0.0.0', 
            port=9090
        )
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return False

def start_auto_booking_system():
    """Start the auto-booking system"""
    print("🤖 Starting Auto-booking System...")
    
    try:
        from auto_booking_engine import initialize_auto_booking
        auto_booking_engine = initialize_auto_booking()
        print("✅ Auto-booking system started")
        return auto_booking_engine
    except Exception as e:
        print(f"❌ Error starting auto-booking: {e}")
        return None

def display_system_status():
    """Display current system status"""
    print("\n" + "=" * 60)
    print("🎯 ENHANCED BOOKING SYSTEM STATUS")
    print("=" * 60)
    
    # Check configuration
    config = verify_configuration()
    print(f"✅ Auto-booking: {'Enabled' if config['booking_preferences']['auto_booking_enabled'] else 'Disabled'}")
    print(f"✅ Monitoring: {'Enabled' if config['booking_preferences']['monitoring_enabled'] else 'Disabled'}")
    print(f"✅ Centers: {len(config['booking_preferences']['preferred_centers'])} configured")
    print(f"✅ Daily Limit: {config['automation_settings']['max_daily_bookings']} bookings")
    print(f"✅ Confidence Threshold: {config['automation_settings']['auto_booking_threshold']}%")
    
    # Check appointments
    try:
        with open('appointments_database.json', 'r') as f:
            data = json.load(f)
            appointments = data.get('appointments', [])
        print(f"✅ Current Appointments: {len(appointments)}")
        
        confirmed = [apt for apt in appointments if apt.get('status') == 'Confirmed']
        print(f"✅ Confirmed Bookings: {len(confirmed)}")
    except:
        print("⚠️ No appointments database found")
    
    print("=" * 60)

def show_access_info():
    """Show how to access the system"""
    print("\n" + "🌐" + " " * 20 + "ACCESS INFORMATION" + " " * 20 + "🌐")
    print("=" * 60)
    print("🎯 Enhanced Dashboard: http://localhost:9090")
    print("🔐 Password: F@padma2041")
    print("📱 Original Dashboard: http://localhost:8090")
    print("=" * 60)
    print("\n📋 SYSTEM FEATURES:")
    print("✅ Real-time slot monitoring")
    print("✅ Automatic booking system")
    print("✅ Multi-center tracking")
    print("✅ Live statistics & analytics")
    print("✅ Booking management")
    print("✅ Secure authentication")
    print("=" * 60)

def main():
    """Main system launcher"""
    print("🚀 ENHANCED BOOKING SYSTEM LAUNCHER")
    print("=" * 60)
    print("Initializing all components...")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Please install missing dependencies first")
        return
    
    # Step 2: Setup directories
    setup_directories()
    
    # Step 3: Verify configuration
    config = verify_configuration()
    
    # Step 4: Initialize database
    initialize_database()
    
    # Step 5: Display system status
    display_system_status()
    
    # Step 6: Show access information
    show_access_info()
    
    print("\n🚀 Starting system components...")
    
    # Step 7: Start auto-booking system in background
    auto_booking_thread = threading.Thread(
        target=start_auto_booking_system, 
        daemon=True
    )
    auto_booking_thread.start()
    
    # Step 8: Start enhanced dashboard (blocking)
    print("\n🎯 Starting Enhanced Dashboard...")
    print("🌐 Access at: http://localhost:9090")
    print("🔐 Password: F@padma2041")
    print("\n" + "=" * 60)
    
    try:
        start_enhanced_dashboard()
    except KeyboardInterrupt:
        print("\n⏹️ System shutdown requested")
    except Exception as e:
        print(f"\n❌ System error: {e}")
    
    print("\n✅ Enhanced Booking System stopped")

if __name__ == "__main__":
    main()
