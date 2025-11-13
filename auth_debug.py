#!/usr/bin/env python3
"""
Quick Authentication Fix & Test
Direct password verification and fix
"""

# Test the authentication logic directly
SYSTEM_PASSWORD = "admin123"

def test_authentication():
    print("🔐 AUTHENTICATION SYSTEM TEST")
    print("=" * 50)
    
    test_passwords = ["admin123", "Admin123", "ADMIN123", "admin", "123", ""]
    
    print(f"✅ System Password Set To: '{SYSTEM_PASSWORD}'")
    print()
    
    for test_pwd in test_passwords:
        result = test_pwd == SYSTEM_PASSWORD
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} Testing: '{test_pwd}' == '{SYSTEM_PASSWORD}' -> {result}")
    
    print()
    print("🔍 DIAGNOSIS:")
    print(f"• Password is case-sensitive")
    print(f"• Exact match required: '{SYSTEM_PASSWORD}'")
    print(f"• No extra spaces allowed")
    
    # Interactive test
    print()
    print("🧪 INTERACTIVE TEST:")
    user_input = input("Enter the password to test: ").strip()
    
    if user_input == SYSTEM_PASSWORD:
        print("✅ SUCCESS! Authentication would work.")
    else:
        print("❌ FAILED! Authentication would fail.")
        print(f"Expected: '{SYSTEM_PASSWORD}'")
        print(f"Got: '{user_input}'")
        print(f"Length expected: {len(SYSTEM_PASSWORD)}")
        print(f"Length got: {len(user_input)}")

if __name__ == "__main__":
    test_authentication()
