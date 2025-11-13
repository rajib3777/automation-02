#!/usr/bin/env python3
"""
Authentication Test Script
=========================

This script tests the authentication system to ensure it's working correctly.
"""

import requests
import json
import time

def test_authentication():
    """Test the authentication system"""
    base_url = "http://localhost:5000"
    
    print("🔐 AUTHENTICATION TEST")
    print("=" * 40)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return
    except requests.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running on localhost:5000")
        print("   Start the app with: python ultra_powerful_app.py")
        return
    except Exception as e:
        print(f"❌ Server connection error: {e}")
        return
    
    # Test 2: Check authentication status before login
    try:
        response = requests.get(f"{base_url}/api/check_auth")
        auth_data = response.json()
        print(f"📊 Initial auth status: {auth_data.get('authenticated', False)}")
    except Exception as e:
        print(f"⚠️ Could not check initial auth status: {e}")
    
    # Test 3: Test with correct password
    print("\n🔑 Testing with correct password: 'admin123'")
    try:
        response = requests.post(
            f"{base_url}/api/popup_auth",
            json={"password": "admin123"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print("✅ Authentication successful with correct password")
                print(f"   Message: {result.get('message')}")
            else:
                print("❌ Authentication failed despite correct password")
                print(f"   Response: {result}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
    
    # Test 4: Test with wrong password
    print("\n🔑 Testing with wrong password: 'wrongpass'")
    try:
        response = requests.post(
            f"{base_url}/api/popup_auth",
            json={"password": "wrongpass"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            result = response.json()
            print("✅ Correctly rejected wrong password")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"⚠️ Unexpected response for wrong password: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Wrong password test error: {e}")
    
    # Test 5: Test different password variations
    print("\n🔑 Testing password variations...")
    test_passwords = [
        "Admin123",  # Different case
        " admin123 ",  # With spaces
        "admin123\n",  # With newline
        "ADMIN123",  # All caps
    ]
    
    for test_pass in test_passwords:
        try:
            response = requests.post(
                f"{base_url}/api/popup_auth",
                json={"password": test_pass},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"⚠️  Password '{repr(test_pass)}' was accepted - this might be unexpected")
            else:
                print(f"✅ Password '{repr(test_pass)}' correctly rejected")
                
        except Exception as e:
            print(f"❌ Error testing password '{test_pass}': {e}")
    
    print("\n📋 SUMMARY")
    print("=" * 40)
    print("✅ Current password: admin123")
    print("✅ Server should be accessible at: http://localhost:5000")
    print("✅ Login by entering 'admin123' in the popup")
    print("\n💡 TROUBLESHOOTING TIPS:")
    print("1. Make sure you're typing exactly: admin123")
    print("2. No extra spaces before or after")
    print("3. Check browser console for JavaScript errors")
    print("4. Try refreshing the page if login popup doesn't appear")
    print("5. Check the server console for authentication debug messages")

if __name__ == "__main__":
    test_authentication()
