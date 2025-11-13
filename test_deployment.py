#!/usr/bin/env python3
"""
Deployment Test Script for Ultra-Powerful Wafid Automation Tool
Tests basic functionality after deployment to verify everything works
"""

import requests
import json
import time
from datetime import datetime

def test_deployment(base_url):
    """Test deployment functionality"""
    print(f"🧪 Testing deployment at: {base_url}")
    print("=" * 60)
    
    tests = []
    
    # Test 1: Health Check
    try:
        print("1️⃣  Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🐍 Environment: {data.get('environment')}")
            tests.append(("Health Check", True))
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            tests.append(("Health Check", False))
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        tests.append(("Health Check", False))
    
    print()
    
    # Test 2: Deployment Info
    try:
        print("2️⃣  Testing deployment info endpoint...")
        response = requests.get(f"{base_url}/api/deployment_info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Deployment info retrieved")
            print(f"   🏗️  Platform: {data.get('platform')}")
            print(f"   🌐 Chrome available: {data.get('chrome_available')}")
            print(f"   🚗 ChromeDriver available: {data.get('chromedriver_available')}")
            tests.append(("Deployment Info", True))
        else:
            print(f"   ❌ Deployment info failed: {response.status_code}")
            tests.append(("Deployment Info", False))
    except Exception as e:
        print(f"   ❌ Deployment info error: {e}")
        tests.append(("Deployment Info", False))
    
    print()
    
    # Test 3: Main Dashboard
    try:
        print("3️⃣  Testing main dashboard...")
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            if "Ultra-Powerful Wafid Automation Tool" in response.text:
                print(f"   ✅ Dashboard loaded successfully")
                print(f"   📄 Page size: {len(response.text)} bytes")
                tests.append(("Main Dashboard", True))
            else:
                print(f"   ❌ Dashboard content incorrect")
                tests.append(("Main Dashboard", False))
        else:
            print(f"   ❌ Dashboard failed: {response.status_code}")
            tests.append(("Main Dashboard", False))
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")
        tests.append(("Main Dashboard", False))
    
    print()
    
    # Test 4: Ultra Stats
    try:
        print("4️⃣  Testing ultra stats endpoint...")
        response = requests.get(f"{base_url}/api/ultra_stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Ultra stats retrieved")
            print(f"   📊 Active sessions: {data.get('active_sessions', 0)}")
            print(f"   🎯 Features active: {len(data.get('ultra_powerful_features', {}))}")
            tests.append(("Ultra Stats", True))
        else:
            print(f"   ❌ Ultra stats failed: {response.status_code}")
            tests.append(("Ultra Stats", False))
    except Exception as e:
        print(f"   ❌ Ultra stats error: {e}")
        tests.append(("Ultra Stats", False))
    
    print()
    
    # Test Results Summary
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    print(f"🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Deployment is successful!")
        print("🚀 Your Ultra-Powerful Wafid Automation Tool is ready!")
    else:
        print("⚠️  Some tests failed. Please check the deployment.")
        print("📖 Refer to DEPLOYMENT_GUIDE.md for troubleshooting.")
    
    print()
    print("🔗 Quick Links:")
    print(f"   🏠 Dashboard: {base_url}")
    print(f"   💚 Health: {base_url}/health")
    print(f"   📊 Stats: {base_url}/api/ultra_stats")
    print(f"   🔧 Deployment Info: {base_url}/api/deployment_info")

if __name__ == "__main__":
    print("🚀 Ultra-Powerful Wafid Automation Tool - Deployment Test")
    print("=" * 60)
    
    # Get base URL from user
    base_url = input("Enter your Render app URL (e.g., https://your-app.onrender.com): ").strip()
    
    if not base_url:
        print("❌ No URL provided. Using example URL for demonstration.")
        base_url = "https://ultra-wafid-automation.onrender.com"
    
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    
    base_url = base_url.rstrip('/')
    
    print(f"🎯 Testing deployment at: {base_url}")
    print()
    
    test_deployment(base_url)
