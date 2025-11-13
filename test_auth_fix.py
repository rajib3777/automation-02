#!/usr/bin/env python3
"""Test Authentication Fix"""

# Exact same logic as in the app
SYSTEM_PASSWORD = "admin123"

def test_password():
    print("🧪 TESTING AUTHENTICATION LOGIC")
    print("=" * 40)
    
    test_inputs = [
        "admin123",
        " admin123",
        "admin123 ",
        " admin123 ",
        "Admin123",
        "ADMIN123",
        ""
    ]
    
    for test_input in test_inputs:
        stripped = test_input.strip()
        result = stripped == SYSTEM_PASSWORD
        status = "✅" if result else "❌"
        
        print(f"{status} Input: {repr(test_input)} -> Stripped: {repr(stripped)} -> Result: {result}")
    
    print()
    print("💡 SOLUTION:")
    print("The correct password is: admin123")
    print("Make sure there are no spaces before or after")

if __name__ == "__main__":
    test_password()
