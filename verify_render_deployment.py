"""
🔍 RENDER DEPLOYMENT VERIFICATION SCRIPT
=======================================
Use this script to verify your Render deployment is working correctly
"""

import requests
import json
import time
from datetime import datetime

def test_deployment(base_url):
    """Test the deployed application"""
    
    print(f"🔍 Testing deployment at: {base_url}")
    print("=" * 50)
    
    # Test 1: Basic connectivity
    print("\n1️⃣ Testing basic connectivity...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Application is accessible")
        else:
            print(f"❌ HTTP {response.status_code}: {response.reason}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test 2: Check if login page loads
    print("\n2️⃣ Testing login page...")
    try:
        if "password" in response.text.lower() or "login" in response.text.lower():
            print("✅ Login page detected")
        else:
            print("⚠️  Login page content unclear")
    except Exception as e:
        print(f"❌ Error checking login page: {e}")
    
    # Test 3: Test authentication endpoint
    print("\n3️⃣ Testing authentication...")
    auth_url = f"{base_url}/authenticate"
    auth_data = {"password": "F@padma2041"}
    
    try:
        auth_response = requests.post(auth_url, json=auth_data, timeout=10)
        if auth_response.status_code == 200:
            result = auth_response.json()
            if result.get("success"):
                print("✅ Authentication successful")
            else:
                print("❌ Authentication failed")
        else:
            print(f"⚠️  Auth endpoint returned {auth_response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not test authentication: {e}")
    
    # Test 4: Check SSL certificate
    print("\n4️⃣ Testing SSL certificate...")
    if base_url.startswith("https://"):
        print("✅ HTTPS enabled")
    else:
        print("⚠️  HTTP only (consider enabling HTTPS)")
    
    # Test 5: Response time
    print("\n5️⃣ Testing response time...")
    start_time = time.time()
    try:
        requests.get(base_url, timeout=10)
        response_time = time.time() - start_time
        print(f"⏱️  Response time: {response_time:.2f} seconds")
        if response_time < 2:
            print("✅ Good response time")
        elif response_time < 5:
            print("⚠️  Acceptable response time")
        else:
            print("❌ Slow response time")
    except Exception as e:
        print(f"❌ Could not measure response time: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 VERIFICATION COMPLETE!")
    return True

def main():
    print("🚀 RENDER DEPLOYMENT VERIFICATION")
    print("=" * 50)
    
    # Get URL from user
    default_url = "https://ultra-powerful-wafid-bot.onrender.com"
    print(f"Default URL: {default_url}")
    
    url = input(f"Enter your Render URL (or press Enter for default): ").strip()
    if not url:
        url = default_url
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    print(f"\n🔗 Testing URL: {url}")
    test_deployment(url)
    
    print("\n📋 POST-VERIFICATION CHECKLIST:")
    print("- [ ] Application loads without errors")
    print("- [ ] Login works with password: F@padma2041")
    print("- [ ] Dashboard functions are accessible")
    print("- [ ] No sensitive information visible")
    print("- [ ] Performance is acceptable")
    print("- [ ] HTTPS is enabled")
    
    print(f"\n📝 Verification completed at: {datetime.now()}")

if __name__ == "__main__":
    main()
