#!/usr/bin/env python3
"""
Wafid Appointment Scheduler
Author: MiniMax Agent

Intelligent scheduling system that runs the booking automation
at optimal times for better success rates.
"""

import schedule
import time
import subprocess
import argparse
import json
import os
from datetime import datetime, timedelta
import logging

class WafidScheduler:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.booking_process = None
        
    def load_config(self, config_file):
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def setup_logging(self):
        """Set up logging for the scheduler."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SCHEDULER - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('wafid_scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_booking_automation(self):
        """Start the booking automation process."""
        try:
            self.logger.info("🚀 Starting scheduled booking automation...")
            
            # Check if process is already running
            if self.booking_process and self.booking_process.poll() is None:
                self.logger.warning("Booking automation already running, skipping this schedule")
                return
            
            # Start the booking automation
            self.booking_process = subprocess.Popen([
                'python3', 'wafid_booking_automation.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.logger.info(f"Booking automation started with PID: {self.booking_process.pid}")
            
        except Exception as e:
            self.logger.error(f"Failed to start booking automation: {e}")
    
    def stop_booking_automation(self):
        """Stop the booking automation process."""
        try:
            if self.booking_process and self.booking_process.poll() is None:
                self.booking_process.terminate()
                self.booking_process.wait(timeout=10)
                self.logger.info("Booking automation stopped")
            else:
                self.logger.info("No active booking automation to stop")
        except Exception as e:
            self.logger.error(f"Failed to stop booking automation: {e}")
    
    def check_booking_status(self):
        """Check if we already have successful bookings."""
        try:
            # Check for recent successful bookings
            result_files = [f for f in os.listdir('.') if f.startswith('booking_results_')]
            if result_files:
                latest_file = max(result_files)
                with open(latest_file, 'r') as f:
                    results = json.load(f)
                
                successful_bookings = len(results.get('successful_bookings', []))
                target_centers = len(self.config.get('booking_preferences', {}).get('preferred_centers', []))
                
                if successful_bookings >= target_centers:
                    self.logger.info("🎉 All target bookings completed! Stopping scheduler.")
                    return True
        except Exception as e:
            self.logger.error(f"Failed to check booking status: {e}")
        
        return False
    
    def peak_hours_job(self):
        """Job to run during peak hours with more frequent attempts."""
        if self.check_booking_status():
            return
        
        self.logger.info("🔥 Peak hours booking attempt...")
        self.run_booking_automation()
    
    def off_peak_job(self):
        """Job to run during off-peak hours."""
        if self.check_booking_status():
            return
        
        self.logger.info("🌙 Off-peak booking attempt...")
        self.run_booking_automation()
    
    def smart_schedule(self):
        """Set up intelligent scheduling based on optimal booking times."""
        self.logger.info("Setting up smart scheduling...")
        
        # Peak hours (higher booking success rates)
        peak_times = [
            "06:00", "06:30", "07:00", "07:30", "08:00",  # Early morning
            "12:00", "12:30", "13:00", "13:30",          # Lunch time
            "18:00", "18:30", "19:00", "19:30", "20:00"  # Evening
        ]
        
        # Off-peak hours
        off_peak_times = [
            "09:00", "10:30", "14:00", "15:30", "16:30", "21:30", "23:00"
        ]
        
        # Schedule peak hour attempts
        for time_slot in peak_times:
            schedule.every().day.at(time_slot).do(self.peak_hours_job)
        
        # Schedule off-peak attempts
        for time_slot in off_peak_times:
            schedule.every().day.at(time_slot).do(self.off_peak_job)
        
        self.logger.info(f"Scheduled {len(peak_times)} peak hour attempts")
        self.logger.info(f"Scheduled {len(off_peak_times)} off-peak attempts")
    
    def custom_schedule(self, start_time, end_time, interval_minutes):
        """Set up custom scheduling with specific times and intervals."""
        from datetime import datetime, timedelta
        
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))
        
        start_dt = datetime.now().replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
        end_dt = datetime.now().replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
        
        current_dt = start_dt
        count = 0
        
        while current_dt <= end_dt:
            time_str = current_dt.strftime("%H:%M")
            schedule.every().day.at(time_str).do(self.run_booking_automation)
            current_dt += timedelta(minutes=interval_minutes)
            count += 1
        
        self.logger.info(f"Scheduled {count} custom attempts between {start_time} and {end_time}")
    
    def run_scheduler(self, mode="smart", start_time=None, end_time=None, interval=60):
        """Run the scheduler with specified mode."""
        self.logger.info(f"🕐 Starting Wafid Appointment Scheduler - Mode: {mode}")
        
        if mode == "smart":
            self.smart_schedule()
        elif mode == "custom" and start_time and end_time:
            self.custom_schedule(start_time, end_time, interval)
        else:
            self.logger.error("Invalid scheduling mode or missing parameters")
            return
        
        self.logger.info("Scheduler running... Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")
            self.stop_booking_automation()
        except Exception as e:
            self.logger.error(f"Scheduler error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Wafid Appointment Scheduler")
    parser.add_argument("--mode", choices=["smart", "custom"], default="smart",
                       help="Scheduling mode (default: smart)")
    parser.add_argument("--start-time", help="Start time for custom mode (HH:MM)")
    parser.add_argument("--end-time", help="End time for custom mode (HH:MM)")
    parser.add_argument("--interval", type=int, default=60,
                       help="Interval in minutes for custom mode (default: 60)")
    parser.add_argument("--config", default="config.json",
                       help="Configuration file path")
    
    args = parser.parse_args()
    
    print("🕐 Wafid Appointment Scheduler")
    print("=" * 40)
    
    if args.mode == "custom" and (not args.start_time or not args.end_time):
        print("❌ Custom mode requires --start-time and --end-time")
        return
    
    scheduler = WafidScheduler(args.config)
    
    if args.mode == "smart":
        print("📅 Smart scheduling mode activated")
        print("   - Optimized for peak booking times")
        print("   - Automatic frequency adjustment")
    else:
        print(f"📅 Custom scheduling mode: {args.start_time} to {args.end_time}")
        print(f"   - Interval: {args.interval} minutes")
    
    print()
    input("Press Enter to start scheduler (Ctrl+C to stop)...")
    
    scheduler.run_scheduler(
        mode=args.mode,
        start_time=args.start_time,
        end_time=args.end_time,
        interval=args.interval
    )


if __name__ == "__main__":
    main()