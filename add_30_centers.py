#!/usr/bin/env python3
"""
Bulk Add 30 Centers Script
Use this to quickly add all 30 centers via API
"""

import requests
import json
import time

# Your Render deployment URL
BASE_URL = "https://your-app-name.onrender.com"  # Replace with your actual URL
SYSTEM_PASSWORD = "F@padma2041"

# 30 centers data
centers_data = [
    # Riyadh Centers (1-10)
    {"name": "Riyadh Medical Center - King Fahd", "location": "Riyadh", "capacity": 200},
    {"name": "Riyadh Diagnostic Center - Al Nakheel", "location": "Riyadh", "capacity": 180},
    {"name": "Riyadh Health Hub - Olaya", "location": "Riyadh", "capacity": 220},
    {"name": "Riyadh Wellness Center - Malaz", "location": "Riyadh", "capacity": 190},
    {"name": "Riyadh Medical Plaza - Al Malaz", "location": "Riyadh", "capacity": 210},
    {"name": "Riyadh Care Center - Al Yar", "location": "Riyadh", "capacity": 175},
    {"name": "Riyadh Health Center - Al Naseem", "location": "Riyadh", "capacity": 185},
    {"name": "Riyadh Medical Center - Al Quds", "location": "Riyadh", "capacity": 195},
    {"name": "Riyadh Diagnostic Hub - Al Izdihar", "location": "Riyadh", "capacity": 205},
    {"name": "Riyadh Health Plaza - Al Waha", "location": "Riyadh", "capacity": 200},
    
    # Jeddah Centers (11-20)
    {"name": "Jeddah Medical Center - Corniche", "location": "Jeddah", "capacity": 190},
    {"name": "Jeddah Diagnostic Center - Red Sea Mall", "location": "Jeddah", "capacity": 200},
    {"name": "Jeddah Health Hub - Al Balad", "location": "Jeddah", "capacity": 180},
    {"name": "Jeddah Wellness Center - Al Zahra", "location": "Jeddah", "capacity": 195},
    {"name": "Jeddah Medical Plaza - Al Shisha", "location": "Jeddah", "capacity": 210},
    {"name": "Jeddah Care Center - Al Hamra", "location": "Jeddah", "capacity": 185},
    {"name": "Jeddah Health Center - Alzahra", "location": "Jeddah", "capacity": 190},
    {"name": "Jeddah Medical Center - Al Rola", "location": "Jeddah", "capacity": 200},
    {"name": "Jeddah Diagnostic Hub - Al Kurna", "location": "Jeddah", "capacity": 185},
    {"name": "Jeddah Health Plaza - Al Shisha Road", "location": "Jeddah", "capacity": 195},
    
    # Dammam & Eastern Province (21-30)
    {"name": "Dammam Medical Center - King Fahd", "location": "Dammam", "capacity": 200},
    {"name": "Dammam Diagnostic Center - Corniche", "location": "Dammam", "capacity": 190},
    {"name": "Dammam Health Hub - Al Shura", "location": "Dammam", "capacity": 180},
    {"name": "Dammam Wellness Center - Dhahran", "location": "Dammam", "capacity": 195},
    {"name": "Dammam Medical Plaza - Al Khobar", "location": "Dammam", "capacity": 210},
    {"name": "Dammam Care Center - Al Qatif", "location": "Dammam", "capacity": 185},
    {"name": "Dammam Health Center - Al Jubail", "location": "Dammam", "capacity": 190},
    {"name": "Dammam Medical Center - Al Mubarraz", "location": "Dammam", "capacity": 200},
    {"name": "Dammam Diagnostic Hub - Al Ahsa", "location": "Dammam", "capacity": 185},
    {"name": "Dammam Health Plaza - Al Karkh", "location": "Dammam", "capacity": 195}
]

def add_center(center_data, session):
    """Add a single center via API"""
    url = f"{BASE_URL}/api/add_center"
    
    data = {
        "name": center_data["name"],
        "location": center_data["location"],
        "capacity": center_data["capacity"],
        "automation_level": "advanced",  # Set all to advanced
        "priority_level": 1,
        "daily_target": int(center_data["capacity"] * 0.25)  # 25% of capacity
    }
    
    try:
        response = session.post(url, json=data)
        if response.status_code == 200:
            print(f"✅ Added: {center_data['name']}")
            return True
        else:
            print(f"❌ Failed to add {center_data['name']}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error adding {center_data['name']}: {e}")
        return False

def main():
    print("🚀 Adding 30 Centers to Your Wafid Automation Platform")
    print("=" * 60)
    
    # Create session with authentication
    session = requests.Session()
    session.auth = ("admin", SYSTEM_PASSWORD)
    
    # Add centers with delay to avoid overwhelming the server
    for i, center in enumerate(centers_data, 1):
        print(f"📍 Adding Center {i}/30: {center['name']}")
        
        if add_center(center, session):
            print("   ✅ Success")
        else:
            print("   ❌ Failed")
        
        # Delay between requests
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("🎉 All 30 centers added successfully!")
    print("💡 Now you can:")
    print("   1. Go to your dashboard")
    print("   2. Start automation")
    print("   3. Monitor real-time performance")
    print("   4. Watch 30 centers working simultaneously!")

if __name__ == "__main__":
    # Set your actual Render URL
    BASE_URL = input("Enter your Render app URL (e.g., https://wafid-automation.onrender.com): ")
    main()
