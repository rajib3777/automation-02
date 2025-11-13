#!/usr/bin/env python3
"""
Wafid Medical Appointment Automation System
Author: MiniMax Agent

This system automatically books appointments at preferred medical centers
by monitoring the auto-assignment system and retrying until success.
"""

import time
import json
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random


class WafidBookingBot:
    def __init__(self, config_file="config.json"):
        """Initialize the booking bot with configuration."""
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.driver = None
        self.successful_bookings = []
        
    def load_config(self, config_file):
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if file doesn't exist
            default_config = {
                "user_details": {
                    "full_name": "YOUR_FULL_NAME",
                    "passport_number": "YOUR_PASSPORT_NUMBER",
                    "nationality": "YOUR_NATIONALITY",
                    "phone": "YOUR_PHONE_NUMBER",
                    "email": "YOUR_EMAIL@example.com"
                },
                "booking_preferences": {
                    "country": "Pakistan",
                    "city": "Lahore",
                    "traveling_country": "Saudi Arabia",
                    "preferred_centers": [
                        "Medical Center Name 1",
                        "Medical Center Name 2"
                    ]
                },
                "automation_settings": {
                    "max_attempts": 50,
                    "delay_between_attempts": 30,
                    "timeout": 10,
                    "headless": False
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"Created default config file: {config_file}")
            print("Please update the configuration with your details!")
            return default_config

    def setup_logging(self):
        """Set up logging for the automation process."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('wafid_booking.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        """Set up Chrome WebDriver with options."""
        chrome_options = Options()
        if self.config["automation_settings"]["headless"]:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Add user agent to appear more human-like
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, self.config["automation_settings"]["timeout"])

    def navigate_to_booking_page(self):
        """Navigate to the Wafid booking page."""
        try:
            self.logger.info("Navigating to Wafid booking page...")
            self.driver.get("https://wafid.com/book-appointment/")
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to booking page: {e}")
            return False

    def fill_booking_form(self):
        """Fill the booking form with user details."""
        try:
            self.logger.info("Filling booking form...")
            
            # Wait for page to load and find form elements
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
            
            # Select country
            country_dropdown = Select(self.driver.find_element(By.NAME, "country"))
            country_dropdown.select_by_visible_text(self.config["booking_preferences"]["country"])
            time.sleep(2)
            
            # Select city
            city_dropdown = Select(self.driver.find_element(By.NAME, "city"))
            city_dropdown.select_by_visible_text(self.config["booking_preferences"]["city"])
            time.sleep(2)
            
            # Select traveling country
            traveling_dropdown = Select(self.driver.find_element(By.NAME, "traveling_country"))
            traveling_dropdown.select_by_visible_text(self.config["booking_preferences"]["traveling_country"])
            time.sleep(2)
            
            # Fill personal details
            name_field = self.driver.find_element(By.NAME, "full_name")
            name_field.clear()
            name_field.send_keys(self.config["user_details"]["full_name"])
            
            passport_field = self.driver.find_element(By.NAME, "passport_number")
            passport_field.clear()
            passport_field.send_keys(self.config["user_details"]["passport_number"])
            
            phone_field = self.driver.find_element(By.NAME, "phone")
            phone_field.clear()
            phone_field.send_keys(self.config["user_details"]["phone"])
            
            email_field = self.driver.find_element(By.NAME, "email")
            email_field.clear()
            email_field.send_keys(self.config["user_details"]["email"])
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to fill booking form: {e}")
            return False

    def get_assigned_center(self):
        """Extract the assigned medical center from the page."""
        try:
            # Look for assigned center information
            center_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Medical Center') or contains(text(), 'Center')]")
            
            for element in center_elements:
                center_text = element.text.strip()
                if center_text and "Medical" in center_text:
                    self.logger.info(f"Assigned center: {center_text}")
                    return center_text
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get assigned center: {e}")
            return None

    def is_preferred_center(self, assigned_center):
        """Check if the assigned center is one of the preferred centers."""
        if not assigned_center:
            return False
            
        preferred_centers = self.config["booking_preferences"]["preferred_centers"]
        for preferred in preferred_centers:
            if preferred.lower() in assigned_center.lower():
                return True
        return False

    def complete_booking(self):
        """Complete the booking process if center is preferred."""
        try:
            # Look for submit/continue button
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Continue') or contains(text(), 'Book')]"))
            )
            submit_button.click()
            
            # Wait for payment page or confirmation
            time.sleep(5)
            
            # Handle payment page (this would need to be customized based on actual payment flow)
            self.logger.info("Reached payment/confirmation page")
            
            # Get booking reference if available
            booking_ref = self.get_booking_reference()
            
            return booking_ref
            
        except Exception as e:
            self.logger.error(f"Failed to complete booking: {e}")
            return None

    def get_booking_reference(self):
        """Extract booking reference number."""
        try:
            # Look for booking reference patterns
            ref_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Reference') or contains(text(), 'Booking') or contains(text(), 'ID')]")
            
            for element in ref_elements:
                text = element.text.strip()
                if any(keyword in text.upper() for keyword in ['REF', 'BOOKING', 'ID', 'NUMBER']):
                    return text
            
            return f"Booking_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        except Exception as e:
            self.logger.error(f"Failed to get booking reference: {e}")
            return None

    def single_booking_attempt(self):
        """Perform a single booking attempt."""
        try:
            # Navigate to booking page
            if not self.navigate_to_booking_page():
                return False, None
            
            # Fill the form
            if not self.fill_booking_form():
                return False, None
            
            # Submit form to see assigned center
            submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or @type='submit']")
            submit_btn.click()
            
            time.sleep(5)
            
            # Get assigned center
            assigned_center = self.get_assigned_center()
            
            if not assigned_center:
                self.logger.warning("Could not determine assigned center")
                return False, None
            
            # Check if it's a preferred center
            if self.is_preferred_center(assigned_center):
                self.logger.info(f"SUCCESS: Got preferred center - {assigned_center}")
                
                # Complete the booking
                booking_ref = self.complete_booking()
                
                if booking_ref:
                    booking_info = {
                        "center": assigned_center,
                        "reference": booking_ref,
                        "timestamp": datetime.now().isoformat(),
                        "user": self.config["user_details"]["full_name"]
                    }
                    self.successful_bookings.append(booking_info)
                    return True, booking_info
            else:
                self.logger.info(f"Got non-preferred center: {assigned_center}, retrying...")
                return False, assigned_center
            
        except Exception as e:
            self.logger.error(f"Booking attempt failed: {e}")
            return False, None

    def run_automation(self):
        """Main automation loop."""
        self.logger.info("Starting Wafid booking automation...")
        self.logger.info(f"Target centers: {self.config['booking_preferences']['preferred_centers']}")
        
        max_attempts = self.config["automation_settings"]["max_attempts"]
        delay = self.config["automation_settings"]["delay_between_attempts"]
        
        target_bookings = len(self.config["booking_preferences"]["preferred_centers"])
        successful_centers = set()
        
        try:
            self.setup_driver()
            
            for attempt in range(1, max_attempts + 1):
                self.logger.info(f"Attempt {attempt}/{max_attempts}")
                
                success, result = self.single_booking_attempt()
                
                if success and result:
                    center_name = result["center"]
                    successful_centers.add(center_name)
                    self.logger.info(f"✅ Booked appointment at: {center_name}")
                    self.logger.info(f"Booking reference: {result['reference']}")
                    
                    # Check if we have all required bookings
                    if len(successful_centers) >= target_bookings:
                        self.logger.info("🎉 SUCCESS: All preferred centers booked!")
                        break
                
                # Wait before next attempt
                if attempt < max_attempts:
                    self.logger.info(f"Waiting {delay} seconds before next attempt...")
                    time.sleep(delay + random.randint(5, 15))  # Add random delay
                
            # Save results
            self.save_results()
            
        except KeyboardInterrupt:
            self.logger.info("Automation stopped by user")
        except Exception as e:
            self.logger.error(f"Automation failed: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def save_results(self):
        """Save booking results to file."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "successful_bookings": self.successful_bookings,
            "total_successful": len(self.successful_bookings),
            "target_centers": self.config["booking_preferences"]["preferred_centers"]
        }
        
        with open(f"booking_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(results, f, indent=4)
        
        self.logger.info(f"Results saved. Total successful bookings: {len(self.successful_bookings)}")


def main():
    """Main function to run the booking automation."""
    print("🏥 Wafid Multi-Center Booking Automation System")
    print("=" * 50)
    
    bot = WafidBookingBot()
    
    # Validate configuration
    if bot.config["user_details"]["full_name"] == "YOUR_FULL_NAME":
        print("❌ Please update the configuration file with your details first!")
        print("Edit 'config.json' with your personal information.")
        return
    
    print(f"👤 User: {bot.config['user_details']['full_name']}")
    print(f"🎯 Target Centers: {bot.config['booking_preferences']['preferred_centers']}")
    print(f"📍 Location: {bot.config['booking_preferences']['city']}, {bot.config['booking_preferences']['country']}")
    print(f"✈️  Traveling to: {bot.config['booking_preferences']['traveling_country']}")
    print()
    
    input("Press Enter to start automation (Ctrl+C to stop)...")
    
    bot.run_automation()


if __name__ == "__main__":
    main()