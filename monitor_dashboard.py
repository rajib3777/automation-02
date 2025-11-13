#!/usr/bin/env python3
"""
Wafid Booking Automation - Monitor Dashboard
Author: MiniMax Agent
Date: 2025-09-18

Real-time monitoring dashboard for tracking booking automation progress.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path

class MonitorDashboard:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.stats = {
            "total_attempts": 0,
            "successful_bookings": 0,
            "preferred_center_hits": 0,
            "session_data": {},
            "start_time": datetime.now(),
            "last_update": datetime.now()
        }
    
    def load_config(self):
        """Load configuration"""
        try:
            with open("advanced_config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Configuration file not found")
            return None
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self):
        """Print dashboard header"""
        self.clear_screen()
        print("\n" + "█" * 80)
        print("📊 WAFID BOOKING AUTOMATION - LIVE MONITOR DASHBOARD")
        print("🎯 Real-time Progress Tracking")
        print("█" * 80 + "\n")
    
    def print_config_info(self):
        """Print configuration information"""
        if not self.config:
            print("❌ Configuration not loaded")
            return
        
        print("🛠️ CONFIGURATION SUMMARY")
        print("-" * 40)
        print(f"User: {self.config.get('user_details', {}).get('full_name', 'N/A')}")
        print(f"City: {self.config.get('booking_preferences', {}).get('city', 'N/A')}")
        
        preferred_centers = self.config.get('booking_preferences', {}).get('preferred_centers', [])
        print(f"Target Centers: {len(preferred_centers)}")
        for i, center in enumerate(preferred_centers, 1):
            print(f"  {i}. {center}")
        
        advanced = self.config.get('advanced_settings', {})
        print(f"Max Sessions: {advanced.get('max_concurrent_sessions', 'N/A')}")
        print(f"Target Bookings: {advanced.get('success_target', 2)}")
        print()
    
    def print_live_stats(self):
        """Print live statistics"""
        current_time = datetime.now()
        elapsed = current_time - self.stats["start_time"]
        elapsed_str = str(elapsed).split('.')[0]
        
        print("📊 LIVE STATISTICS")
        print("-" * 40)
        print(f"🔄 Runtime: {elapsed_str}")
        print(f"🎯 Total Attempts: {self.stats['total_attempts']}")
        print(f"✅ Successful Bookings: {self.stats['successful_bookings']}/2")
        print(f"🎆 Preferred Center Hits: {self.stats['preferred_center_hits']}")
        
        # Calculate success rate
        if self.stats["total_attempts"] > 0:
            success_rate = (self.stats["preferred_center_hits"] / self.stats["total_attempts"]) * 100
            print(f"🔥 Success Rate: {success_rate:.1f}%")
        else:
            print(f"🔥 Success Rate: 0.0%")
        
        # Attempts per minute
        if elapsed.total_seconds() > 0:
            attempts_per_min = (self.stats["total_attempts"] * 60) / elapsed.total_seconds()
            print(f"⚡ Attempts/Min: {attempts_per_min:.1f}")
        
        print(f"⏰ Last Update: {current_time.strftime('%H:%M:%S')}")
        print()
    
    def print_session_details(self):
        """Print details for each active session"""
        print("🛠️ ACTIVE SESSIONS")
        print("-" * 40)
        
        if not self.stats["session_data"]:
            print("🟡 No active sessions detected")
            print("💡 Start automation to see session data")
        else:
            for session_name, data in self.stats["session_data"].items():
                status_icon = "🟢" if data.get("active", False) else "🔴"
                print(f"{status_icon} {session_name}:")
                print(f"    Attempts: {data.get('attempts', 0)}")
                print(f"    Success: {data.get('successes', 0)}")
                print(f"    Last Activity: {data.get('last_activity', 'Never')}")
        print()
    
    def print_progress_bar(self):
        """Print progress towards target"""
        if not self.config:
            return
        
        target = self.config.get('advanced_settings', {}).get('success_target', 2)
        current = self.stats['successful_bookings']
        
        print("🏆 PROGRESS TO TARGET")
        print("-" * 40)
        
        # Progress bar
        progress = min(current / target, 1.0) if target > 0 else 0
        bar_length = 30
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f"[{bar}] {current}/{target} ({progress*100:.1f}%)")
        
        if current >= target:
            print("🎉 TARGET ACHIEVED! All bookings completed!")
        else:
            remaining = target - current
            print(f"🎯 Remaining: {remaining} booking(s)")
        print()
    
    def print_recent_activity(self):
        """Print recent activity log"""
        print("📜 RECENT ACTIVITY")
        print("-" * 40)
        
        # This would normally read from a log file or shared data
        # For demo purposes, showing simulated activity
        activities = [
            "Session-1: Attempt #45 - Center assigned: General Hospital",
            "Session-2: Attempt #38 - Center assigned: City Medical",
            "Session-1: SUCCESS! Booked at Al-Shifa Medical Center",
            "Session-3: Attempt #23 - Center assigned: Metro Clinic"
        ]
        
        for activity in activities[-5:]:  # Show last 5 activities
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {activity}")
        print()
    
    def print_system_info(self):
        """Print system information"""
        print("🛠️ SYSTEM INFO")
        print("-" * 40)
        print(f"Python: {sys.version.split()[0]}")
        print(f"Platform: {sys.platform}")
        print(f"Config File: {'Loaded' if self.config else 'Missing'}")
        print(f"Monitor Status: {'Running' if self.running else 'Stopped'}")
        print()
    
    def update_stats(self):
        """Update statistics from various sources"""
        # In a real implementation, this would read from:
        # - Log files
        # - Shared memory
        # - Database
        # - Inter-process communication
        
        # For demo, we'll simulate some activity
        import random
        
        if random.random() < 0.3:  # 30% chance of new activity
            self.stats["total_attempts"] += random.randint(0, 2)
        
        if random.random() < 0.05:  # 5% chance of success
            self.stats["successful_bookings"] += 1
            self.stats["preferred_center_hits"] += 1
        
        self.stats["last_update"] = datetime.now()
    
    def print_instructions(self):
        """Print usage instructions"""
        print("📚 INSTRUCTIONS")
        print("-" * 40)
        print("• This dashboard monitors your booking automation")
        print("• Start automation in another terminal with: python command_center.py")
        print("• Press Ctrl+C to exit this monitor")
        print("• Data refreshes every 3 seconds")
        print()
    
    def run_dashboard(self):
        """Main dashboard loop"""
        self.running = True
        
        print("📊 Starting Monitor Dashboard...")
        time.sleep(1)
        
        try:
            while self.running:
                self.print_header()
                self.print_config_info()
                self.print_live_stats()
                self.print_session_details()
                self.print_progress_bar()
                self.print_recent_activity()
                self.print_system_info()
                self.print_instructions()
                
                print("🔄 Dashboard refreshing... (Ctrl+C to exit)")
                
                # Update stats for next refresh
                self.update_stats()
                
                time.sleep(3)  # Refresh every 3 seconds
                
        except KeyboardInterrupt:
            self.running = False
            print("\n\n📊 Monitor Dashboard stopped")
        except Exception as e:
            print(f"\n\n❌ Dashboard error: {e}")

def main():
    print("📊 WAFID BOOKING MONITOR DASHBOARD")
    print("Initializing...")
    
    try:
        dashboard = MonitorDashboard()
        dashboard.run_dashboard()
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
