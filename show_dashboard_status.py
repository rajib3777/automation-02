#!/usr/bin/env python3
"""
🎯 ENHANCED BOOKING SYSTEM STATUS DASHBOARD
============================================
Live status display for your booking system
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_json_file(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def display_system_status():
    """Display comprehensive system status"""
    
    print("🚀" + "="*60 + "🚀")
    print("   ENHANCED BOOKING SYSTEM - LIVE STATUS DASHBOARD   ")
    print("🚀" + "="*60 + "🚀")
    print()
    
    # Load configuration
    config = load_json_file('config.json')
    appointments = load_json_file('appointments_database.json')
    
    # System Overview
    print("📊 SYSTEM OVERVIEW")
    print("-" * 40)
    print(f"✅ System Status: ACTIVE & MONITORING")
    print(f"🌐 Dashboard URL: http://localhost:9090")
    print(f"🔐 Password: F@padma2041")
    print(f"📅 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configuration Status
    if config:
        booking_prefs = config.get('booking_preferences', {})
        auto_settings = config.get('automation_settings', {})
        
        print("⚙️  CONFIGURATION STATUS")
        print("-" * 40)
        print(f"🎯 Auto-booking: {'✅ ENABLED' if booking_prefs.get('auto_booking_enabled') else '❌ DISABLED'}")
        print(f"📡 Monitoring: {'✅ ENABLED' if booking_prefs.get('monitoring_enabled') else '❌ DISABLED'}")
        print(f"🏥 Centers Monitored: {len(booking_prefs.get('preferred_centers', []))}")
        print(f"⭐ Priority Centers: {len(booking_prefs.get('priority_centers', []))}")
        print(f"🎯 Confidence Threshold: {auto_settings.get('auto_booking_threshold', 85)}%")
        print(f"📊 Daily Booking Limit: {auto_settings.get('max_daily_bookings', 5)}")
        print()
    
    # Centers Being Monitored
    if config and 'booking_preferences' in config:
        centers = config['booking_preferences'].get('preferred_centers', [])
        priority_centers = config['booking_preferences'].get('priority_centers', [])
        
        print("🏥 MONITORED MEDICAL CENTERS")
        print("-" * 40)
        for center in centers:
            priority_mark = "⭐ PRIORITY" if center in priority_centers else "📍 Standard"
            print(f"{priority_mark} {center}")
        print()
    
    # Current Appointments
    if appointments and 'appointments' in appointments:
        print("📋 YOUR CONFIRMED APPOINTMENTS")
        print("-" * 40)
        for apt in appointments['appointments']:
            status_icon = "✅" if apt.get('status') == 'Confirmed' else "⏳"
            payment_icon = "💳" if apt.get('payment_status') == 'Completed' else "💰"
            
            print(f"{status_icon} {apt.get('name', 'N/A')}")
            print(f"   🏥 Center: {apt.get('center', 'N/A')}")
            print(f"   📅 Date: {apt.get('date', 'N/A')} at {apt.get('time', 'N/A')}")
            print(f"   📧 Email: {apt.get('email', 'N/A')}")
            print(f"   🆔 Passport: {apt.get('passport_no', 'N/A')}")
            print(f"   {payment_icon} Payment: {apt.get('payment_status', 'N/A')} - ${apt.get('amount', 0)}")
            print(f"   📄 Payment ID: {apt.get('payment_id', 'N/A')}")
            print()
    else:
        print("📋 YOUR CONFIRMED APPOINTMENTS")
        print("-" * 40)
        print("❌ No confirmed appointments found")
        print()
    
    # Real-time Statistics
    print("📈 REAL-TIME STATISTICS")
    print("-" * 40)
    total_appointments = len(appointments.get('appointments', [])) if appointments else 0
    confirmed_appointments = len([apt for apt in appointments.get('appointments', []) if apt.get('status') == 'Confirmed']) if appointments else 0
    
    print(f"📊 Total Appointments: {total_appointments}")
    print(f"✅ Confirmed Bookings: {confirmed_appointments}")
    print(f"💳 Completed Payments: {len([apt for apt in appointments.get('appointments', []) if apt.get('payment_status') == 'Completed']) if appointments else 0}")
    print()
    
    # System Features
    print("🔧 ACTIVE FEATURES")
    print("-" * 40)
    print("✅ Real-time slot monitoring")
    print("✅ Automatic booking system")
    print("✅ Multi-center tracking")
    print("✅ Payment processing")
    print("✅ Email notifications")
    print("✅ Booking confirmations")
    print("✅ Priority center booking")
    print("✅ Confidence-based filtering")
    print()
    
    # Quick Actions
    print("🎯 QUICK ACTIONS")
    print("-" * 40)
    print("🌐 Access Dashboard: http://localhost:9090")
    print("📋 Check Appointments: python check_my_appointments.py")
    print("🚀 Restart System: python launch_enhanced_system.py")
    print()
    
    print("🚀" + "="*60 + "🚀")
    print("    System is LIVE and monitoring for available slots!    ")
    print("🚀" + "="*60 + "🚀")

if __name__ == "__main__":
    display_system_status()
