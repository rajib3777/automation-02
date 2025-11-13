#!/usr/bin/env python3
"""
Password Configuration Check
===========================

Quick verification that the password is correctly configured.
"""

def check_password_config():
    """Check the current password configuration"""
    print("🔐 PASSWORD CONFIGURATION CHECK")
    print("=" * 50)
    
    try:
        # Read the password from the app file
        with open('ultra_powerful_app.py', 'r') as f:
            content = f.read()
            
        # Find the password line
        for line_num, line in enumerate(content.split('\n'), 1):
            if 'SYSTEM_PASSWORD' in line and '=' in line and not line.strip().startswith('#'):
                print(f"✅ Found password configuration on line {line_num}:")
                print(f"   {line.strip()}")
                
                # Extract password
                if '"' in line:
                    password = line.split('"')[1]
                elif "'" in line:
                    password = line.split("'")[1]
                else:
                    password = "Could not extract"
                
                print(f"\n🔑 Current Password: {password}")
                break
        
        print("\n📋 AUTHENTICATION INSTRUCTIONS")
        print("-" * 30)
        print("1. 🚀 Start the application:")
        print("   python ultra_powerful_app.py")
        print()
        print("2. 🌐 Open your browser and go to:")
        print("   http://localhost:5000")
        print()
        print("3. 🔓 When the login popup appears, enter:")
        print(f"   {password}")
        print()
        print("4. ✅ The system should unlock and show the dashboard")
        
        print("\n🔧 TROUBLESHOOTING")
        print("-" * 20)
        print("• Make sure you type the password exactly as shown")
        print("• No extra spaces before or after the password")
        print("• Check that JavaScript is enabled in your browser")
        print("• If popup doesn't appear, refresh the page")
        print("• Check browser console (F12) for any JavaScript errors")
        
        print("\n💡 TESTING")
        print("-" * 10)
        print("• Run 'python auth_test.py' after starting the server")
        print("• This will test the authentication system automatically")
        
        return password
        
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return None

if __name__ == "__main__":
    check_password_config()
