#!/usr/bin/env python3
"""
EMERGENCY AUTHENTICATION FIX
Direct fix for authentication issues
"""

import re

def fix_authentication():
    print("🚨 EMERGENCY AUTHENTICATION FIX")
    print("=" * 50)
    
    # Read the current ultra_powerful_app.py
    try:
        with open('/workspace/ultra_powerful_app.py', 'r') as f:
            content = f.read()
        
        # Check current password setting
        password_match = re.search(r'SYSTEM_PASSWORD\s*=\s*["\']([^"\']*)["\']', content)
        if password_match:
            current_password = password_match.group(1)
            print(f"🔍 Current password found: '{current_password}'")
        else:
            print("❌ No password found in file")
            return
        
        # Fix any potential issues
        fixed_content = content
        
        # Make sure password is exactly 'admin123'
        fixed_content = re.sub(
            r'SYSTEM_PASSWORD\s*=\s*["\'][^"\']*["\']',
            'SYSTEM_PASSWORD = "admin123"',
            fixed_content
        )
        
        # Add debug logging to authentication function
        auth_function_pattern = r'(@app\.route\(\'/api/popup_auth\', methods=\[\'POST\'\]\)\ndef popup_auth\(\):.*?)(if password == SYSTEM_PASSWORD:)'
        
        debug_code = '''        # EMERGENCY DEBUG - Remove after fixing
        print(f"🐛 RAW PASSWORD INPUT: {repr(password)}")
        print(f"🐛 STRIPPED PASSWORD: {repr(password.strip())}")
        print(f"🐛 SYSTEM PASSWORD: {repr(SYSTEM_PASSWORD)}")
        print(f"🐛 COMPARISON RESULT: {password == SYSTEM_PASSWORD}")
        print(f"🐛 STRIPPED COMPARISON: {password.strip() == SYSTEM_PASSWORD}")
        
        # Use stripped password for comparison
        password = password.strip()
        
        '''
        
        if 'EMERGENCY DEBUG' not in fixed_content:
            fixed_content = re.sub(
                r'(if password == SYSTEM_PASSWORD:)',
                debug_code + r'\1',
                fixed_content
            )
        
        # Write the fixed content back
        with open('/workspace/ultra_powerful_app.py', 'w') as f:
            f.write(fixed_content)
        
        print("✅ Applied emergency fix to ultra_powerful_app.py")
        print("🔧 Changes made:")
        print("  - Set password to exactly 'admin123'")
        print("  - Added debug logging")
        print("  - Added password stripping")
        
    except Exception as e:
        print(f"❌ Error applying fix: {e}")
        return
    
    # Create a simple test script
    test_script = '''#!/usr/bin/env python3
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
'''
    
    with open('/workspace/test_auth_fix.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created test script: test_auth_fix.py")
    
    # Create an HTML standalone test
    html_test = '''<!DOCTYPE html>
<html>
<head>
    <title>Authentication Test - Standalone</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background: #f5f5f5; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .password-hint { background: #e3f2fd; padding: 15px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #2196f3; }
        input[type="password"] { width: 100%; padding: 12px; margin: 10px 0; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        .test-btn { background: #4caf50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
        .test-btn:hover { background: #45a049; }
        .result { margin: 20px 0; padding: 15px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Emergency Authentication Test</h1>
        
        <div class="password-hint">
            <strong>💡 Password:</strong> admin123<br>
            <small>Case sensitive, no spaces allowed</small>
        </div>
        
        <input type="password" id="testPassword" placeholder="Enter password to test">
        <button class="test-btn" onclick="testAuth()">Test Authentication</button>
        
        <div id="result"></div>
        
        <div style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <h3>🔧 Debug Information:</h3>
            <p><strong>Expected:</strong> admin123 (exactly)</p>
            <p><strong>Case Sensitive:</strong> Yes</p>
            <p><strong>Spaces:</strong> Will be automatically stripped</p>
        </div>
    </div>

    <script>
        function testAuth() {
            const input = document.getElementById('testPassword').value;
            const resultDiv = document.getElementById('result');
            const expected = 'admin123';
            
            // Show debug info
            const stripped = input.trim();
            const matches = stripped === expected;
            
            let html = '<h3>🧪 Test Results:</h3>';
            html += `<p><strong>Your Input:</strong> "${input}"</p>`;
            html += `<p><strong>After Trimming:</strong> "${stripped}"</p>`;
            html += `<p><strong>Expected:</strong> "${expected}"</p>`;
            html += `<p><strong>Matches:</strong> ${matches}</p>`;
            
            if (matches) {
                html += '<p><strong>✅ SUCCESS!</strong> This password should work.</p>';
                resultDiv.className = 'result success';
            } else {
                html += '<p><strong>❌ FAILED!</strong> Password incorrect.</p>';
                resultDiv.className = 'result error';
            }
            
            resultDiv.innerHTML = html;
        }
        
        // Allow Enter key
        document.getElementById('testPassword').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                testAuth();
            }
        });
    </script>
</body>
</html>'''
    
    with open('/workspace/auth_test.html', 'w') as f:
        f.write(html_test)
    
    print("✅ Created standalone HTML test: auth_test.html")
    print()
    print("🚀 NEXT STEPS:")
    print("1. Run: python test_auth_fix.py")
    print("2. Open auth_test.html in browser")
    print("3. Try the original app again")
    print()
    print("📋 SUMMARY:")
    print("✅ Emergency fix applied")
    print("✅ Debug logging added")
    print("✅ Test tools created")

if __name__ == "__main__":
    fix_authentication()
