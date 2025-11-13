#!/usr/bin/env python3
"""
NO-AUTH VERSION - EMERGENCY BYPASS
Version of the dashboard without authentication requirements
"""

# Simple HTTP server that serves the dashboard without authentication
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

PORT = 9000

class NoAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/dashboard':
            self.serve_dashboard()
        elif self.path.startswith('/static/'):
            self.serve_static_file()
        else:
            self.send_404()
    
    def serve_dashboard(self):
        try:
            # Read the original dashboard HTML
            with open('/workspace/templates/ultra_powerful_dashboard.html', 'r') as f:
                html_content = f.read()
            
            # Remove authentication overlay and requirements
            # Replace authentication popup with a simple "No Auth Required" message
            no_auth_html = html_content.replace(
                'showAuthenticationPopup();',
                '// Authentication bypassed in no-auth version'
            ).replace(
                'checkAuthenticationOnLoad()',
                'unlockSystemDirectly()'
            )
            
            # Add JavaScript to auto-unlock
            auto_unlock_script = """
<script>
function unlockSystemDirectly() {
    console.log('🔓 No-Auth Mode: Auto-unlocking system');
    
    // Hide auth overlay
    const overlay = document.getElementById('authOverlay');
    if (overlay) overlay.style.display = 'none';
    
    // Hide system locked indicator
    const indicator = document.getElementById('systemLockedIndicator');
    if (indicator) indicator.style.display = 'none';
    
    // Unlock main content
    const mainContent = document.getElementById('mainContent');
    if (mainContent) mainContent.classList.add('unlocked');
    
    // Set authentication state
    window.isAuthenticated = true;
    
    // Add success message
    addActivity('🎉 No-Auth Mode: System ready!', 'success');
    
    console.log('✅ System unlocked in no-auth mode');
}

// Override auth check functions
function is_authenticated() { return true; }
function checkAuthenticationOnLoad() { unlockSystemDirectly(); }
function showAuthenticationPopup() { 
    console.log('Authentication popup blocked in no-auth mode'); 
    unlockSystemDirectly();
}
</script>
"""
            
            # Insert the script before closing body tag
            no_auth_html = no_auth_html.replace('</body>', auto_unlock_script + '</body>')
            
            # Add a banner indicating no-auth mode
            no_auth_banner = '''
<div style="background: #ff9800; color: white; padding: 10px; text-align: center; font-weight: bold;">
    🔓 NO-AUTH MODE - Authentication Bypassed for Testing
</div>
'''
            
            no_auth_html = no_auth_html.replace('<body>', '<body>' + no_auth_banner)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(no_auth_html.encode())
            
        except Exception as e:
            self.send_error(500, f"Error serving dashboard: {str(e)}")
    
    def serve_static_file(self):
        self.send_404()
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>404 - Not Found</h1>')
    
    def do_POST(self):
        # Handle any POST requests by returning success
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "success", "message": "No-auth mode: Operation simulated"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_404()

def run_no_auth_server():
    server = HTTPServer(('localhost', PORT), NoAuthHandler)
    print(f"🚀 NO-AUTH DASHBOARD SERVER")
    print(f"📍 Running on: http://localhost:{PORT}")
    print(f"🔓 Authentication: BYPASSED")
    print(f"💡 This version works without any password")
    print(f"🌐 Open your browser to: http://localhost:{PORT}")
    print()
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 No-auth server stopped")

if __name__ == "__main__":
    run_no_auth_server()
