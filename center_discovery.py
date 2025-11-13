#!/usr/bin/env python3
"""
Wafid Medical Center Discovery Tool
Author: MiniMax Agent

Helps users discover the exact names of medical centers
available in their city for accurate configuration.
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import argparse
from datetime import datetime

class CenterDiscovery:
    def __init__(self):
        self.driver = None
        self.centers_found = set()
        
    def setup_driver(self, headless=True):
        """Set up Chrome WebDriver."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def discover_centers(self, country, city, traveling_country="Saudi Arabia", attempts=20):
        """Discover medical centers by making multiple booking attempts."""
        print(f"🔍 Discovering medical centers in {city}, {country}")
        print(f"Target destination: {traveling_country}")
        print(f"Running {attempts} discovery attempts...")
        print()
        
        try:
            self.setup_driver()
            
            for attempt in range(1, attempts + 1):
                print(f"Attempt {attempt}/{attempts}...", end=" ")
                
                try:
                    # Navigate to booking page
                    self.driver.get("https://wafid.com/book-appointment/")
                    time.sleep(3)
                    
                    # Fill location details
                    country_dropdown = Select(self.driver.find_element(By.NAME, "country"))
                    country_dropdown.select_by_visible_text(country)
                    time.sleep(2)
                    
                    city_dropdown = Select(self.driver.find_element(By.NAME, "city"))
                    city_dropdown.select_by_visible_text(city)
                    time.sleep(2)
                    
                    traveling_dropdown = Select(self.driver.find_element(By.NAME, "traveling_country"))
                    traveling_dropdown.select_by_visible_text(traveling_country)
                    time.sleep(2)
                    
                    # Fill dummy personal details
                    name_field = self.driver.find_element(By.NAME, "full_name")
                    name_field.clear()
                    name_field.send_keys("Test User")
                    
                    passport_field = self.driver.find_element(By.NAME, "passport_number")
                    passport_field.clear()
                    passport_field.send_keys("AB1234567")
                    
                    phone_field = self.driver.find_element(By.NAME, "phone")
                    phone_field.clear()
                    phone_field.send_keys("+92-300-1234567")
                    
                    email_field = self.driver.find_element(By.NAME, "email")
                    email_field.clear()
                    email_field.send_keys("test@example.com")
                    
                    # Submit to see assigned center
                    submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or @type='submit']")
                    submit_btn.click()
                    
                    time.sleep(5)
                    
                    # Look for assigned center
                    center_name = self.extract_center_name()
                    
                    if center_name:
                        if center_name not in self.centers_found:
                            print(f"NEW: {center_name}")
                            self.centers_found.add(center_name)
                        else:
                            print(f"Found: {center_name}")
                    else:
                        print("No center detected")
                    
                    # Wait between attempts
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error: {str(e)[:50]}...")
                    continue
            
            # Display results
            self.display_results(city, country)
            
        except Exception as e:
            print(f"Discovery failed: {e}")
        finally:
            if self.driver:
                self.driver.quit()
    
    def extract_center_name(self):
        """Extract medical center name from the page."""
        try:
            # Common patterns for center information
            selectors = [
                "//*[contains(text(), 'Medical Center')]",
                "//*[contains(text(), 'Hospital')]",
                "//*[contains(text(), 'Clinic')]",
                "//*[contains(text(), 'assigned')]",
                "//*[contains(text(), 'Center')]",
                "//div[@class='center-info']//text()",
                "//span[@class='center-name']//text()",
                "//p[contains(@class, 'center')]//text()"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and any(keyword in text.lower() for keyword in ['medical', 'hospital', 'clinic', 'center']):
                            # Clean up the text
                            if 'assigned' in text.lower():
                                # Extract center name after "assigned to"
                                parts = text.split(':')
                                if len(parts) > 1:
                                    return parts[1].strip()
                            elif len(text) > 5 and len(text) < 100:
                                return text
                except:
                    continue
                    
            return None
            
        except Exception as e:
            return None
    
    def display_results(self, city, country):
        """Display discovered centers."""
        print()
        print("=" * 60)
        print(f"🏥 DISCOVERED MEDICAL CENTERS IN {city.upper()}, {country.upper()}")
        print("=" * 60)
        
        if self.centers_found:
            print(f"Found {len(self.centers_found)} unique medical centers:")
            print()
            
            for i, center in enumerate(sorted(self.centers_found), 1):
                print(f"{i:2d}. {center}")
            
            print()
            print("📋 Configuration Template:")
            print("-" * 30)
            
            config_template = {
                "booking_preferences": {
                    "country": country,
                    "city": city,
                    "traveling_country": "Saudi Arabia",
                    "preferred_centers": list(sorted(self.centers_found))[:2]
                }
            }
            
            print(json.dumps(config_template, indent=4))
            
            # Save to file
            filename = f"centers_{city.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            full_results = {
                "discovery_info": {
                    "city": city,
                    "country": country,
                    "discovery_date": datetime.now().isoformat(),
                    "total_centers_found": len(self.centers_found)
                },
                "centers": list(sorted(self.centers_found)),
                "config_template": config_template
            }
            
            with open(filename, 'w') as f:
                json.dump(full_results, f, indent=4)
            
            print()
            print(f"💾 Results saved to: {filename}")
            
        else:
            print("❌ No medical centers were discovered.")
            print("This could be due to:")
            print("- Incorrect city/country names")
            print("- Website changes")
            print("- Network issues")
            print("- Form validation requirements")
        
        print()
        print("💡 Tips:")
        print("- Use exact city and country names as they appear on Wafid")
        print("- Try different spelling variations if no centers found")
        print("- Copy the exact center names to your config.json")


def main():
    parser = argparse.ArgumentParser(description="Discover Wafid Medical Centers")
    parser.add_argument("--city", required=True, help="City name (e.g., 'Lahore')")
    parser.add_argument("--country", required=True, help="Country name (e.g., 'Pakistan')")
    parser.add_argument("--traveling-to", default="Saudi Arabia", help="Destination country")
    parser.add_argument("--attempts", type=int, default=20, help="Number of discovery attempts")
    parser.add_argument("--headless", action="store_true", help="Run browser in background")
    
    args = parser.parse_args()
    
    print("🔍 Wafid Medical Center Discovery Tool")
    print("=" * 40)
    print()
    
    discovery = CenterDiscovery()
    discovery.discover_centers(
        country=args.country,
        city=args.city,
        traveling_country=args.traveling_to,
        attempts=args.attempts
    )


if __name__ == "__main__":
    main()