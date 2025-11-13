from flask import Flask, render_template, jsonify
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-key'

# Simple data
stats = {
    'total_bookings': 0,
    'daily_bookings': 0,
    'success_rate': 85.0,
    'monitoring_active': False,
    'auto_booking_active': False,
    'system_uptime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

centers = {
    'precision': {'name': 'Precision Diagnostics Ltd', 'active': True, 'success_rate': 85},
    'mediquest': {'name': 'Mediquest Diagnostics Ltd', 'active': True, 'success_rate': 75},
    'allied': {'name': 'Allied Diagnostics Ltd', 'active': True, 'success_rate': 65}
}

config = {
    "user_details": {
        "full_name": "Farid Hossain",
        "passport_number": "AE5241562",
        "nationality": "Bangladesh",
        "phone": "+8801234567890",
        "email": "mominit8@gmail.com"
    },
    "booking_preferences": {
        "country": "Pakistan", 
        "city": "Lahore",
        "max_daily_bookings": 100
    }
}

appointments = [
    {
        "id": "1",
        "center": "Precision Diagnostics Ltd",
        "user_name": "Farid Hossain", 
        "booking_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "confirmed"
    }
]

@app.route('/')
def index():
    """Main dashboard - NO AUTHENTICATION"""
    try:
        return render_template('ultra_powerful_dashboard.html',
                             config=config,
                             appointments=appointments,
                             target_centers=centers,
                             enhanced_stats=stats,
                             monitoring_active=False,
                             auto_booking_active=False,
                             authenticated=True)
    except Exception as e:
        return f"""
        <html><body>
        <h1>🚀 Ultra-Powerful Wafid System</h1>
        <h2>Dashboard Loading...</h2>
        <p><strong>Status:</strong> Active</p>
        <p><strong>Total Bookings:</strong> {stats['total_bookings']}</p>
        <p><strong>Success Rate:</strong> {stats['success_rate']}%</p>
        <p><strong>Error:</strong> {str(e)}</p>
        <br>
        <button onclick="location.reload()">Refresh</button>
        </body></html>
        """

@app.route('/dashboard')
def dashboard():
    """Dashboard route"""
    return index()

@app.route('/api/get_enhanced_stats')
def get_stats():
    """Get statistics"""
    stats['current_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'enhanced_stats': stats, 'target_centers': centers})

@app.route('/api/start_monitoring', methods=['POST'])
def start_monitoring():
    """Start monitoring"""
    stats['monitoring_active'] = True
    return jsonify({'success': True, 'message': 'Monitoring started'})

@app.route('/api/stop_monitoring', methods=['POST'])
def stop_monitoring():
    """Stop monitoring"""
    stats['monitoring_active'] = False
    return jsonify({'success': True, 'message': 'Monitoring stopped'})

@app.route('/api/start_auto_booking', methods=['POST'])
def start_auto_booking():
    """Start auto booking"""
    stats['auto_booking_active'] = True
    return jsonify({'success': True, 'message': 'Auto-booking started'})

@app.route('/api/stop_auto_booking', methods=['POST'])
def stop_auto_booking():
    """Stop auto booking"""
    stats['auto_booking_active'] = False
    return jsonify({'success': True, 'message': 'Auto-booking stopped'})

@app.route('/api/get_appointments')
def get_appointments():
    """Get appointments"""
    return jsonify({'appointments': appointments})

if __name__ == '__main__':
    print("🚀 ULTRA-POWERFUL WAFID SYSTEM - EMERGENCY VERSION")
    print("✅ NO AUTHENTICATION REQUIRED")
    print("🌐 Direct Dashboard Access")
    app.run(host='0.0.0.0', port=5000, debug=False)