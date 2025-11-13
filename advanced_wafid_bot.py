#!/usr/bin/env python3
"""
Wafid Booking Automation - Advanced Bot
Author: MiniMax Agent
Date: 2025-09-18

Advanced automation bot with concurrent sessions and intelligent retry logic.
"""

import os
import sys
import json
import time
import random
import argparse
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class AdvancedWafidBot:
    def __init__(self, config_file="advanced_config.json", session_name="Main"):
        self.session_name = session_name
        self.config = self.load_config(config_file)
        self.driver = None
        self.stats = {
            "attempts": 0,
            "successes": 0,
            "preferred_hits": 0,
            "start_time": datetime.now()
        }
        self.setup_driver()
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Config file {config_file} not found")
            sys.exit(1)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with optimal settings"""
        chrome_options = Options()
        
        # Stealth settings to avoid detection
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        try:
            # Try to use local chromedriver first
            if os.path.exists("chromedriver"):
                self.driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
            elif os.path.exists("chromedriver.exe"):
                self.driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
            else:
                # Use webdriver-manager as fallback
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"✅ {self.session_name}: Chrome driver initialized")
            
        except Exception as e:
            print(f"❌ {self.session_name}: Failed to initialize Chrome driver: {e}")
            sys.exit(1)
    
    def log(self, message):
        """Log message with timestamp and session name"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.session_name}: {message}")
    
    def navigate_to_booking_page(self):
        """Navigate to the Wafid booking page"""
        self.log("Navigating to Wafid booking page...")
        try:
            self.driver.get("https://wafid.com/book-appointment/")
            time.sleep(random.uniform(2, 4))  # Random delay
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            self.log("✅ Page loaded successfully")
            return True
            
        except TimeoutException:
            self.log("❌ Page load timeout")
            return False
        except Exception as e:
            self.log(f"❌ Navigation error: {e}")
            return False
    
    def fill_booking_form(self):
        """Fill the booking form with user details"""
        self.log("Filling booking form...")
        
        try:
            user_details = self.config["user_details"]
            preferences = self.config["booking_preferences"]
            
            # Fill form fields (adjust selectors based on actual website)
            # This is a template - actual selectors need to be determined from the website
            
            # Name field
            name_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "full_name"))  # Adjust selector
            )
            name_field.clear()
            name_field.send_keys(user_details["full_name"])
            time.sleep(random.uniform(0.5, 1.5))
            
            # Passport field
            passport_field = self.driver.find_element(By.NAME, "passport_number")  # Adjust selector
            passport_field.clear()
            passport_field.send_keys(user_details["passport_number"])
            time.sleep(random.uniform(0.5, 1.5))
            
            # Country dropdown
            country_dropdown = Select(self.driver.find_element(By.NAME, "country"))  # Adjust selector
            country_dropdown.select_by_visible_text(preferences["country"])
            time.sleep(random.uniform(1, 2))
            
            # City dropdown
            city_dropdown = Select(self.driver.find_element(By.NAME, "city"))  # Adjust selector
            city_dropdown.select_by_visible_text(preferences["city"])
            time.sleep(random.uniform(1, 2))
            
            # Additional fields as needed...
            
            self.log("✅ Form filled successfully")
            return True
            
        except TimeoutException:
            self.log("❌ Form filling timeout - elements not found")
            return False
        except Exception as e:
            self.log(f"❌ Form filling error: {e}")
            return False
    
    def submit_and_check_center(self):
        """Submit form and check if assigned center is preferred"""
        self.log("Submitting form and checking assigned center...")
        
        try:
            # Submit form
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Wait for results
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "appointment-details"))  # Adjust selector
            )
            
            # Extract assigned center name
            assigned_center_element = self.driver.find_element(By.CLASS_NAME, "medical-center-name")  # Adjust selector
            assigned_center = assigned_center_element.text.strip()
            
            self.log(f"Assigned center: {assigned_center}")
            
            # Check if it's a preferred center
            preferred_centers = self.config["booking_preferences"]["preferred_centers"]
            
            for preferred in preferred_centers:
                if preferred.lower() in assigned_center.lower():
                    self.log(f"✅ SUCCESS! Got preferred center: {assigned_center}")
                    self.stats["successes"] += 1
                    self.stats["preferred_hits"] += 1
                    return True, assigned_center
            
            self.log(f"❌ Not preferred center: {assigned_center}")
            return False, assigned_center
            
        except TimeoutException:
            self.log("❌ Submission timeout - no results")
            return False, None
        except Exception as e:
            self.log(f"❌ Submission error: {e}")
            return False, None
    
    def cancel_booking(self):
        """Cancel the current booking to try again"""
        self.log("Canceling booking to retry...")
        try:
            # Look for cancel/back button
            cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
            cancel_button.click()
            time.sleep(random.uniform(1, 3))
            return True
        except:
            # If no cancel button, navigate back to booking page
            self.driver.get("https://wafid.com/book-appointment/")
            time.sleep(random.uniform(2, 4))
            return True
    
    def attempt_booking(self):
        """Single booking attempt"""
        self.stats["attempts"] += 1
        attempt_num = self.stats["attempts"]
        
        self.log(f"Starting attempt #{attempt_num}")
        
        # Navigate to booking page
        if not self.navigate_to_booking_page():
            return False, None
        
        # Fill form
        if not self.fill_booking_form():
            return False, None
        
        # Submit and check
        success, center = self.submit_and_check_center()
        
        if success:
            self.log(f"🎉 BOOKING SECURED at {center}!")
            return True, center
        else:
            # Cancel and retry
            self.cancel_booking()
            return False, center
    
    def run_automation(self):
        """Main automation loop"""
        self.log("🚀 Starting Wafid booking automation")
        
        max_attempts = self.config["advanced_settings"]["max_attempts_per_session"]
        retry_delay = self.config["advanced_settings"]["retry_delay_seconds"]
        success_target = self.config["advanced_settings"]["success_target"]
        
        while self.stats["successes"] < success_target and self.stats["attempts"] < max_attempts:
            try:
                success, center = self.attempt_booking()
                
                if success:
                    self.log(f"🎆 Target achieved! Successes: {self.stats['successes']}/{success_target}")
                    if self.stats["successes"] >= success_target:
                        break
                
                # Delay before next attempt
                if self.stats["attempts"] < max_attempts:
                    delay = retry_delay + random.uniform(0, 3)  # Add randomness
                    self.log(f"Waiting {delay:.1f}s before next attempt...")
                    time.sleep(delay)
                
            except KeyboardInterrupt:
                self.log("⏹️ Automation stopped by user")
                break
            except Exception as e:
                self.log(f"❌ Error in attempt #{self.stats['attempts']}: {e}")
                time.sleep(retry_delay)
        
        self.print_final_stats()
    
    def print_final_stats(self):
        """Print final statistics"""
        runtime = datetime.now() - self.stats["start_time"]
        
        print("\n" + "="*50)
        print(f"📊 {self.session_name} - FINAL STATISTICS")
        print("="*50)
        print(f"Runtime: {str(runtime).split('.')[0]}")
        print(f"Total Attempts: {self.stats['attempts']}")
        print(f"Successful Bookings: {self.stats['successes']}")
        print(f"Preferred Center Hits: {self.stats['preferred_hits']}")
        if self.stats["attempts"] > 0:
            success_rate = (self.stats["preferred_hits"] / self.stats["attempts"]) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        print("="*50)
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.log("Browser closed")

def main():
    parser = argparse.ArgumentParser(description="Wafid Booking Automation")
    parser.add_argument("--session", default="Main", help="Session name")
    parser.add_argument("--config", default="advanced_config.json", help="Config file path")
    
    args = parser.parse_args()
    
    bot = None
    try:
        bot = AdvancedWafidBot(args.config, args.session)
        bot.run_automation()
    except KeyboardInterrupt:
        print("\n⏹️ Automation interrupted")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        if bot:
            bot.cleanup()

if __name__ == "__main__":
    main()
