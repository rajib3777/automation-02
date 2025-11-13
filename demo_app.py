"""
Simple Demo Version - Popup Authentication System
===============================================
This is a simplified version to demonstrate the popup authentication functionality
without complex dependencies.
"""

from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultra-powerful-wafid-2025-quantum'

# Authentication Configuration
SYSTEM_PASSWORD = "F@padma2041"  # Default system password
SESSION_TIMEOUT = 3600  # 1 hour session timeout

def is_authenticated():
    """Check if user is authenticated"""
    if 'authenticated' not in session:
        return False
    
    # Check session timeout
    if 'login_time' in session:
        login_time = session['login_time']
        if (datetime.now() - datetime.fromtimestamp(login_time)).seconds > SESSION_TIMEOUT:
            session.clear()
            return False
    
    return session.get('authenticated', False)

@app.route('/')
def ultra_dashboard():
    """Ultra-powerful dashboard - loads with popup authentication"""
    return render_template('ultra_powerful_dashboard.html')

@app.route('/api/popup_auth', methods=['POST'])
def popup_auth():
    """Handle popup authentication"""
    try:
        data = request.json
        password = data.get('password', '')
        
        if password == SYSTEM_PASSWORD:
            session['authenticated'] = True
            session['login_time'] = datetime.now().timestamp()
            session['user_type'] = 'admin'
            
            return jsonify({
                "status": "success",
                "message": "System unlocked successfully!",
                "authenticated": True
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Invalid password. System remains locked."
            }), 401
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Handle logout"""
    session.clear()
    return jsonify({
        "status": "success",
        "message": "Logged out successfully. System locked."
    })

@app.route('/api/check_auth')
def check_auth():
    """Check authentication status"""
    return jsonify({
        "authenticated": is_authenticated(),
        "session_info": {
            "login_time": session.get('login_time'),
            "user_type": session.get('user_type', 'guest')
        } if is_authenticated() else None
    })

@app.route('/api/demo_action', methods=['POST'])
def demo_action():
    """Demo API action that requires authentication"""
    if not is_authenticated():
        return jsonify({"error": "Authentication required"}), 401
    
    action = request.json.get('action', 'unknown')
    return jsonify({
        "status": "success",
        "message": f"Demo action '{action}' executed successfully!",
        "timestamp": datetime.now().isoformat(),
        "authenticated": True
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Ultra-Powerful Wafid Automation Tool - Demo",
        "version": "2025.1.0",
        "timestamp": datetime.now().isoformat(),
        "authentication": {
            "enabled": True,
            "session_timeout": SESSION_TIMEOUT,
            "secure_login": True
        }
    })

if __name__ == '__main__':
    print("🚀 ULTRA-POWERFUL WAFID BOT 2025 - DEMO EDITION")
    print("=" * 50)
    print("✅ Popup Authentication System Active")
    print("✅ Session Management Enabled")
    print("✅ Secure Access Control")
    print(f"✅ Default Password: {SYSTEM_PASSWORD}")
    print("=" * 50)
    print("🌐 Starting server on http://localhost:5000")
    print("🔒 System will be locked on startup - enter password to unlock!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
