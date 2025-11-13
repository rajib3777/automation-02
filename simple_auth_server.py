#!/usr/bin/env python3
"""
Simple Authentication Server
Quick fix for authentication issues
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import os

SYSTEM_PASSWORD = "F@padma2041"  # Secure password
PORT = 8090

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Authentication Test</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 50px; }}
        .container {{ max-width: 400px; margin: 0 auto; text-align: center; }}
        input[type="password"] {{ padding: 10px; margin: 10px; width: 200px; }}
        button {{ padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }}
        .success {{ color: green; font-weight: bold; }}
        .error {{ color: red; font-weight: bold; }}
        .hint {{ background: #f0f8ff; padding: 10px; margin: 10px 0; border-left: 4px solid #007cba; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Authentication Test</h1>
        <div class="hint">
            <strong>💡 Info:</strong> Enter the secure system password
        </div>
        
        <form id="authForm">
            <div>
                <input type="password" id="password" placeholder="Enter password" required>
            </div>
            <div>
                <button type="submit">Test Authentication</button>
            </div>
        </form>
        
        <div id="result"></div>
        
        <div style="margin-top: 30px; text-align: left;">
            <h3>🧪 Security Information:</h3>
            <p><strong>Authentication:</strong> Secure password required</p>
            <p><strong>Case Sensitive:</strong> Yes</p>
            <p><strong>Spaces:</strong> Automatically trimmed</p>
        </div>
    </div>

    <script>
        document.getElementById('authForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const resultDiv = document.getElementById('result');
            
            fetch('/auth', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{password: password}})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    resultDiv.innerHTML = '<div class="success">✅ ' + data.message + '</div>';
                }} else {{
                    resultDiv.innerHTML = '<div class="error">❌ ' + data.message + '</div>';
                }}
            }})
            .catch(error => {{
                resultDiv.innerHTML = '<div class="error">❌ Connection error</div>';
                console.error('Error:', error);
            }});
        }});
    </script>
</body>
</html>
            """
            
            self.wfile.write(html.encode())
    
    def do_POST(self):
        if self.path == '/auth':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                password = data.get('password', '')
                
                print("🔐 Authentication attempt received")
                print(f"🔐 Password length: {len(password)}")
                print(f"🔐 Authentication result: {'Success' if password.strip() == SYSTEM_PASSWORD else 'Failed'}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Trim whitespace from password
                password = password.strip()
                
                if password == SYSTEM_PASSWORD:
                    response = {
                        "success": True,
                        "message": "Authentication successful! Access granted."
                    }
                    print("✅ Authentication SUCCESS")
                else:
                    response = {
                        "success": False,
                        "message": "Authentication failed. Invalid password."
                    }
                    print("❌ Authentication FAILED")
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Error: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"success": False, "message": f"Server error: {str(e)}"}
                self.wfile.write(json.dumps(response).encode())

def run_server():
    server = HTTPServer(('localhost', PORT), AuthHandler)
    print(f"🚀 Authentication Server running on http://localhost:{PORT}")
    print(f"🔐 Secure authentication enabled")
    print(f"💡 Open your browser to access the system")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server()
