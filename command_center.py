#!/usr/bin/env python3
"""
Wafid Booking Automation - Command Center
Author: MiniMax Agent
Date: 2025-09-18

Central control system for managing Wafid booking automation.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime
import subprocess
from pathlib import Path

# Import center code handler
try:
    from center_code_handler import CenterCodeHandler
except ImportError:
    CenterCodeHandler = None

class WafidCommandCenter:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.sessions = []
        self.stats = {
            "total_attempts": 0,
            "successful_bookings": 0,
            "preferred_center_hits": 0,
            "start_time": None,
            "last_success": None
        }
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open("advanced_config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Error: advanced_config.json not found")
            print("💡 Run DEPLOY_NOW.py or live_deploy.py first")
            sys.exit(1)
    
    def print_banner(self):
        """Display system banner"""
        os.system('clear' if os.name != 'nt' else 'cls')
        print("\n" + "="*70)
        print("🎯 WAFID BOOKING AUTOMATION - COMMAND CENTER")
        print("   Maximizing Success for Your Medical Appointments")
        print("="*70)
        print(f"Target Centers: {', '.join(self.config['booking_preferences']['preferred_centers'])}")
        print(f"City: {self.config['booking_preferences']['city']}")
        print(f"Max Sessions: {self.config['advanced_settings']['max_concurrent_sessions']}")
        print("="*70 + "\n")
    
    def show_menu(self):
        """Display main menu"""
        print("🛠️ COMMAND CENTER MENU")
        print("\n1. 🚀 Start Full Automation")
        print("2. 📊 Monitor Dashboard")
        print("3. ⚙️ Configuration")
        print("4. 🔍 System Status")
        print("5. 📊 Success Optimizer")
        print("6. ⏹️ Stop All Sessions")
        print("7. 🚪 Exit")
        
        return input("\nSelect option (1-7): ").strip()
    
    def start_automation(self):
        """Start the full automation system"""
        print("\n🚀 STARTING WAFID BOOKING AUTOMATION")
        print("="*50)
        
        max_sessions = self.config['advanced_settings']['max_concurrent_sessions']
        print(f"Launching {max_sessions} concurrent booking sessions...")
        
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        # Start multiple booking sessions
        for i in range(max_sessions):
            session_thread = threading.Thread(
                target=self.run_booking_session, 
                args=(f"Session-{i+1}",),
                daemon=True
            )
            session_thread.start()
            self.sessions.append(session_thread)
            time.sleep(2)  # Stagger session starts
        
        print(f"\n✅ {len(self.sessions)} sessions launched successfully")
        print("\n📊 LIVE PROGRESS MONITOR:")
        print("-" * 50)
        
        # Monitor progress
        self.monitor_sessions()
    
    def run_booking_session(self, session_name):
        """Run a single booking session"""
        try:
            # This would normally launch the actual bot
            # For demo purposes, we'll simulate the process
            subprocess.run([
                sys.executable, "advanced_wafid_bot.py", 
                "--session", session_name,
                "--config", "advanced_config.json"
            ])
        except Exception as e:
            print(f"❌ {session_name} error: {e}")
    
    def monitor_sessions(self):
        """Monitor active sessions with real-time updates"""
        try:
            while self.running:
                self.update_stats_display()
                time.sleep(5)
        except KeyboardInterrupt:
            self.stop_automation()
    
    def update_stats_display(self):
        """Update real-time statistics display"""
        current_time = datetime.now()
        if self.stats["start_time"]:
            elapsed = current_time - self.stats["start_time"]
            elapsed_str = str(elapsed).split('.')[0]
        else:
            elapsed_str = "00:00:00"
        
        # Clear previous stats (move cursor up)
        print("\033[F" * 8, end="")
        
        print(f"🔄 Runtime: {elapsed_str}")
        print(f"🎯 Total Attempts: {self.stats['total_attempts']}")
        print(f"✅ Successful Bookings: {self.stats['successful_bookings']}/2")
        print(f"🎆 Preferred Centers Hit: {self.stats['preferred_center_hits']}")
        print(f"🔍 Active Sessions: {len([s for s in self.sessions if s.is_alive()])}")
        print(f"🔥 Success Rate: {self.calculate_success_rate():.1f}%")
        print(f"⏰ Last Update: {current_time.strftime('%H:%M:%S')}")
        print("-" * 50)
    
    def calculate_success_rate(self):
        """Calculate current success rate"""
        if self.stats["total_attempts"] == 0:
            return 0.0
        return (self.stats["preferred_center_hits"] / self.stats["total_attempts"]) * 100
    
    def show_dashboard(self):
        """Launch monitoring dashboard"""
        print("\n📊 Launching Monitor Dashboard...")
        try:
            subprocess.run([sys.executable, "monitor_dashboard.py"])
        except FileNotFoundError:
            print("❌ monitor_dashboard.py not found")
        except KeyboardInterrupt:
            print("\n📊 Dashboard closed")
    
    def show_configuration(self):
        """Display current configuration"""
        print("\n⚙️ CURRENT CONFIGURATION")
        print("="*40)
        print(f"User: {self.config['user_details']['full_name']}")
        print(f"City: {self.config['booking_preferences']['city']}")
        print(f"Preferred Centers:")
        
        # Enhanced center display with codes
        centers = self.config['booking_preferences']['preferred_centers']
        center_codes = self.config['booking_preferences'].get('center_codes', {})
        
        for i, center in enumerate(centers, 1):
            code = center_codes.get(center, "")
            code_info = f" (Code: {code})" if code else " (No code)"
            priority_info = "🎯 " if code else "   "
            print(f"  {i}. {priority_info}{center}{code_info}")
        
        print(f"Max Sessions: {self.config['advanced_settings']['max_concurrent_sessions']}")
        print(f"AI Optimization: {self.config['advanced_settings']['enable_ai_optimization']}")
        
        # Show enhanced targeting if available
        if center_codes:
            print(f"\n🎯 Enhanced Center Targeting: ENABLED")
            coded_centers = [c for c, code in center_codes.items() if code]
            if coded_centers:
                print(f"   Precise targeting for: {', '.join(coded_centers)}")
        
        edit = input("\nEdit configuration? (y/n): ").lower().strip()
        if edit == 'y':
            subprocess.run([sys.executable, "live_deploy.py"])
    
    def show_status(self):
        """Show system status"""
        print("\n🔍 SYSTEM STATUS")
        print("="*30)
        print(f"Configuration: {'✅ Loaded' if self.config else '❌ Missing'}")
        print(f"ChromeDriver: {'✅ Ready' if self.check_chromedriver() else '❌ Missing'}")
        print(f"Dependencies: {'✅ Installed' if self.check_dependencies() else '❌ Missing'}")
        print(f"Active Sessions: {len([s for s in self.sessions if s.is_alive()])}")
        print(f"System Status: {'🟢 Running' if self.running else '🔴 Stopped'}")
    
    def check_chromedriver(self):
        """Check if ChromeDriver is available"""
        return os.path.exists("chromedriver") or os.path.exists("chromedriver.exe")
    
    def check_dependencies(self):
        """Check if required packages are installed"""
        try:
            import selenium
            import requests
            import bs4
            return True
        except ImportError:
            return False
    
    def run_optimizer(self):
        """Run success optimizer"""
        print("\n📊 Launching Success Optimizer...")
        try:
            subprocess.run([sys.executable, "success_optimizer.py"])
        except FileNotFoundError:
            print("❌ success_optimizer.py not found")
            print("💡 This feature will be available in future updates")
    
    def stop_automation(self):
        """Stop all automation sessions"""
        print("\n⏹️ Stopping all sessions...")
        self.running = False
        
        # Wait for threads to finish
        for session in self.sessions:
            if session.is_alive():
                session.join(timeout=1)
        
        print("✅ All sessions stopped")
        self.sessions.clear()
    
    def run(self):
        """Main command center loop"""
        while True:
            self.print_banner()
            
            choice = self.show_menu()
            
            if choice == "1":
                self.start_automation()
            elif choice == "2":
                self.show_dashboard()
            elif choice == "3":
                self.show_configuration()
            elif choice == "4":
                self.show_status()
            elif choice == "5":
                self.run_optimizer()
            elif choice == "6":
                self.stop_automation()
            elif choice == "7":
                if self.running:
                    self.stop_automation()
                print("\n👋 Goodbye! Your bookings are our priority.")
                break
            else:
                print("❌ Invalid option. Please try again.")
            
            if choice != "1":  # Don't pause after automation (it has its own loop)
                input("\nPress Enter to continue...")

def main():
    try:
        command_center = WafidCommandCenter()
        command_center.run()
    except KeyboardInterrupt:
        print("\n\n⏹️ System interrupted by user")
    except Exception as e:
        print(f"\n❌ System error: {e}")
        print("💡 Please check your configuration and try again")

if __name__ == "__main__":
    main()
