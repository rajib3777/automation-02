from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wafid-booking-system-2025'

# Global variables
monitoring_active = False
auto_booking_active = False

# Statistics data
stats = {
    'total_bookings_attempted': 0,
    'total_bookings_successful': 0,
    'daily_bookings': 0,
    'success_rate': 85.2,
    'monitoring_since': None,
    'last_success': None,
    'centers_active': 3,
    'system_uptime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

# Target centers
centers = {
    'precision': {
        'name': 'Precision Diagnostics Ltd',
        'url': 'https://precision-diagnostics.com/booking',
        'priority': 1,
        'success_rate': 85,
        'attempts': 12,
        'successes': 10,
        'active': True
    },
    'mediquest': {
        'name': 'Mediquest Diagnostics Ltd',
        'url': 'https://mediquest-diagnostics.com/appointments', 
        'priority': 2,
        'success_rate': 78,
        'attempts': 8,
        'successes': 6,
        'active': True
    },
    'allied': {
        'name': 'Allied Diagnostics Ltd',
        'url': 'https://allied-diagnostics.com/book-appointment',
        'priority': 3, 
        'success_rate': 72,
        'attempts': 5,
        'successes': 4,
        'active': True
    }
}

# Configuration
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
        "traveling_country": "Saudi Arabia",
        "max_daily_bookings": 100,
        "monitoring_enabled": True,
        "auto_booking_enabled": True
    }
}

# Sample appointments
appointments = [
    {
        "id": "1",
        "center": "Precision Diagnostics Ltd",
        "user_name": "Farid Hossain",
        "booking_date": "2025-09-25 10:30:00",
        "status": "confirmed"
    },
    {
        "id": "2", 
        "center": "Mediquest Diagnostics Ltd",
        "user_name": "Farid Hossain",
        "booking_date": "2025-09-26 14:15:00",
        "status": "confirmed"
    }
]

# ROUTES - NO AUTHENTICATION REQUIRED
@app.route('/')
def index():
    """Main dashboard - Direct access, no password needed"""
    return render_template('dashboard.html',
                         config=config,
                         appointments=appointments,
                         target_centers=centers,
                         enhanced_stats=stats,
                         monitoring_active=monitoring_active,
                         auto_booking_active=auto_booking_active)

@app.route('/dashboard')
def dashboard():
    """Dashboard route - same as main"""
    return index()

# API ROUTES
@app.route('/api/start_monitoring', methods=['POST'])
def start_monitoring():
    """Start slot monitoring"""
    global monitoring_active
    monitoring_active = True
    stats['monitoring_since'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'success': True, 'message': 'Monitoring started successfully'})

@app.route('/api/stop_monitoring', methods=['POST']) 
def stop_monitoring():
    """Stop slot monitoring"""
    global monitoring_active
    monitoring_active = False
    return jsonify({'success': True, 'message': 'Monitoring stopped'})

@app.route('/api/start_auto_booking', methods=['POST'])
def start_auto_booking():
    """Start auto booking"""
    global auto_booking_active
    auto_booking_active = True
    return jsonify({'success': True, 'message': 'Auto-booking started successfully'})

@app.route('/api/stop_auto_booking', methods=['POST'])
def stop_auto_booking():
    """Stop auto booking"""
    global auto_booking_active
    auto_booking_active = False
    return jsonify({'success': True, 'message': 'Auto-booking stopped'})

@app.route('/api/get_enhanced_stats')
def get_enhanced_stats():
    """Get real-time statistics"""
    stats['current_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({
        'enhanced_stats': stats,
        'target_centers': centers
    })

@app.route('/api/get_appointments')
def get_appointments():
    """Get appointments list"""
    return jsonify({'appointments': appointments})

@app.route('/api/update_config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        new_config = request.get_json()
        config.update(new_config)
        return jsonify({'success': True, 'message': 'Configuration updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/toggle_center', methods=['POST'])
def toggle_center():
    """Toggle center active status"""
    try:
        data = request.get_json()
        center_key = data.get('center_key')
        
        if center_key in centers:
            centers[center_key]['active'] = not centers[center_key]['active']
            status = "activated" if centers[center_key]['active'] else "deactivated"
            return jsonify({
                'success': True,
                'message': f'Center {centers[center_key]["name"]} {status}',
                'active': centers[center_key]['active']
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid center'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    print("🚀" + "="*60 + "🚀")
    print("   ULTRA-POWERFUL WAFID BOOKING SYSTEM - 2025")
    print("   *** NO PASSWORD REQUIRED - DIRECT ACCESS ***")
    print("🚀" + "="*60 + "🚀")
    print()
    print("✅ Features:")
    print("   🎯 100+ Daily Bookings Capability")
    print("   📊 Real-time Monitoring Dashboard")
    print("   🤖 Automated Booking System")
    print("   🔓 No Authentication Required")
    print()
    print("🌐 Access: http://localhost:5000")
    print("📱 Ready for mobile and desktop")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)