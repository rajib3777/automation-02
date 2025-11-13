#!/usr/bin/env python3
"""
Wafid Booking Automation - Center Code Handler
Author: MiniMax Agent
Date: 2025-09-18

Enhanced center targeting using specific center codes.
"""

import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class CenterCodeHandler:
    def __init__(self, config):
        self.config = config
        self.center_codes = config.get("booking_preferences", {}).get("center_codes", {})
    
    def get_preferred_centers_with_codes(self):
        """Get preferred centers with their codes"""
        preferred = self.config.get("booking_preferences", {}).get("preferred_centers", [])
        centers_with_codes = []
        
        for center in preferred:
            code = self.center_codes.get(center, "")
            centers_with_codes.append({
                "name": center,
                "code": code,
                "has_code": bool(code)
            })
        
        return centers_with_codes
    
    def select_center_by_code(self, driver, target_code):
        """Select center using specific code"""
        try:
            # Look for center dropdown/selection
            center_dropdown = driver.find_element(By.NAME, "medical_center")  # Adjust selector
            
            if center_dropdown.tag_name.lower() == "select":
                select = Select(center_dropdown)
                
                # Try to select by value (code)
                try:
                    select.select_by_value(target_code)
                    return True
                except:
                    pass
                
                # Try to find option with code in text
                for option in select.options:
                    if target_code in option.text or target_code in option.get_attribute("value"):
                        option.click()
                        return True
            
            return False
            
        except Exception as e:
            print(f"Error selecting center by code: {e}")
            return False
    
    def verify_selected_center(self, driver):
        """Verify which center is currently selected"""
        try:
            # Multiple ways to check selected center
            selectors = [
                "//span[@class='selected-center']",
                "//div[@class='appointment-center']",
                "//input[@name='selected_center']",
                "//select[@name='medical_center']"
            ]
            
            for selector in selectors:
                try:
                    element = driver.find_element(By.XPATH, selector)
                    
                    if element.tag_name.lower() == "select":
                        select = Select(element)
                        selected_option = select.first_selected_option
                        return {
                            "name": selected_option.text,
                            "code": selected_option.get_attribute("value"),
                            "element": element
                        }
                    else:
                        return {
                            "name": element.text,
                            "code": element.get_attribute("data-code") or "",
                            "element": element
                        }
                        
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"Error verifying selected center: {e}")
            return None
    
    def is_preferred_center(self, center_info):
        """Check if the selected center is one of our preferred ones"""
        if not center_info:
            return False
        
        center_name = center_info.get("name", "").lower()
        center_code = center_info.get("code", "")
        
        preferred_centers = self.get_preferred_centers_with_codes()
        
        for preferred in preferred_centers:
            # Check by code (most accurate)
            if preferred["code"] and center_code == preferred["code"]:
                return True, preferred["name"]
            
            # Check by name (fallback)
            if preferred["name"].lower() in center_name or center_name in preferred["name"].lower():
                return True, preferred["name"]
        
        return False, None

def load_center_config():
    """Load center configuration with codes"""
    try:
        with open("advanced_config.json", "r") as f:
            config = json.load(f)
        
        print("✅ Center Configuration Loaded:")
        handler = CenterCodeHandler(config)
        centers = handler.get_preferred_centers_with_codes()
        
        for center in centers:
            code_info = f" (Code: {center['code']})" if center["has_code"] else " (No code)"
            print(f"  • {center['name']}{code_info}")
        
        return config
        
    except FileNotFoundError:
        print("❌ Configuration file not found")
        return None

if __name__ == "__main__":
    print("🎯 WAFID CENTER CODE HANDLER")
    print("=" * 40)
    
    config = load_center_config()
    
    if config:
        handler = CenterCodeHandler(config)
        
        print(f"\n🏥 Your Preferred Centers:")
        centers = handler.get_preferred_centers_with_codes()
        
        for i, center in enumerate(centers, 1):
            print(f"{i}. {center['name']}")
            if center['has_code']:
                print(f"   ✅ Code: {center['code']} (Precise targeting enabled)")
            else:
                print(f"   ⚠️  No code (Name-based matching)")
        
        print(f"\n🚀 Enhanced targeting active for centers with codes!")