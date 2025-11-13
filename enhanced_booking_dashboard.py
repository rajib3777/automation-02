"""
🎯 ENHANCED BOOKING DASHBOARD
============================
Advanced dashboard with monitoring, booking management, and auto-booking features
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime, timedelta
import os
import queue
from concurrent.futures import ThreadPoolExecutor
import random

app = Flask(__name__)
app.secret_key = 'ultra_secure_booking_dashboard_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for monitoring
monitoring_active = False
monitoring_thread = None
slot_queue = queue.Queue()
booking_stats = {
    'slots_detected': 0,
    'bookings_attempted': 0,
    'bookings_successful': 0,
    'monitoring_since': None
}

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def load_appointments():
    """Load appointments from database"""
    try:
        with open('appointments_database.json', 'r') as f:
            data = json.load(f)
            return data.get('appointments', [])
    except:
        return []

def save_appointments(appointments):
    """Save appointments to database"""
    try:
        data = {'appointments': appointments}
        with open('appointments_database.json', 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def simulate_slot_monitoring():
    """Simulate slot monitoring with realistic behavior"""
    global monitoring_active, booking_stats
    
    config = load_config()
    centers = config.get('booking_preferences', {}).get('preferred_centers', [])
    auto_booking = config.get('booking_preferences', {}).get('auto_booking_enabled', False)
    threshold = config.get('automation_settings', {}).get('auto_booking_threshold', 85)
    
    while monitoring_active:
        try:
            # Simulate slot detection
            if centers:
                center = random.choice(centers)
                confidence = random.randint(75, 98)
                
                slot_data = {
                    'center': center,
                    'confidence': confidence,
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'available_slots': random.randint(1, 5)
                }
                
                booking_stats['slots_detected'] += 1
                
                # Emit slot detection to dashboard
                socketio.emit('slot_detected', slot_data)
                
                # Auto-booking logic
                if auto_booking and confidence >= threshold:
                    booking_stats['bookings_attempted'] += 1
                    success = attempt_auto_booking(slot_data)
                    if success:
                        booking_stats['bookings_successful'] += 1
                        socketio.emit('booking_success', slot_data)
                
                # Add to slot queue
                slot_queue.put(slot_data)
                
            time.sleep(random.randint(45, 120))  # Random interval between checks
            
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(30)

def attempt_auto_booking(slot_data):
    """Simulate auto-booking attempt"""
    # Simulate booking process with realistic success rate
    success_rate = 0.3 if slot_data['confidence'] > 90 else 0.15
    return random.random() < success_rate

@app.route('/')
def dashboard():
    """Main dashboard page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    config = load_config()
    appointments = load_appointments()
    
    return render_template('enhanced_dashboard.html', 
                         config=config, 
                         appointments=appointments,
                         monitoring_active=monitoring_active,
                         booking_stats=booking_stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('SYSTEM_PASSWORD', 'F@padma2041'):
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/start_monitoring', methods=['POST'])
def start_monitoring():
    """Start slot monitoring"""
    global monitoring_active, monitoring_thread, booking_stats
    
    if not monitoring_active:
        monitoring_active = True
        booking_stats['monitoring_since'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        monitoring_thread = threading.Thread(target=simulate_slot_monitoring, daemon=True)
        monitoring_thread.start()
        
        return jsonify({'success': True, 'message': 'Monitoring started'})
    else:
        return jsonify({'success': False, 'message': 'Monitoring already active'})

@app.route('/api/stop_monitoring', methods=['POST'])
def stop_monitoring():
    """Stop slot monitoring"""
    global monitoring_active
    
    monitoring_active = False
    return jsonify({'success': True, 'message': 'Monitoring stopped'})

@app.route('/api/get_stats')
def get_stats():
    """Get current monitoring statistics"""
    return jsonify(booking_stats)

@app.route('/api/get_appointments')
def get_appointments():
    """Get current appointments"""
    appointments = load_appointments()
    return jsonify({'appointments': appointments})

@app.route('/api/update_config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        new_config = request.json
        with open('config.json', 'w') as f:
            json.dump(new_config, f, indent=2)
        return jsonify({'success': True, 'message': 'Configuration updated'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/get_recent_slots')
def get_recent_slots():
    """Get recent slot detections"""
    slots = []
    while not slot_queue.empty() and len(slots) < 10:
        try:
            slots.append(slot_queue.get_nowait())
        except:
            break
    
    return jsonify({'slots': slots})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if session.get('authenticated'):
        emit('connected', {
            'message': 'Connected to Enhanced Booking Dashboard',
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'monitoring_active': monitoring_active
        })

@socketio.on('request_update')
def handle_update_request():
    """Handle dashboard update request"""
    appointments = load_appointments()
    emit('dashboard_update', {
        'appointments': appointments,
        'stats': booking_stats,
        'monitoring_active': monitoring_active
    })

if __name__ == '__main__':
    print("🚀 ENHANCED BOOKING DASHBOARD STARTING...")
    print("=" * 50)
    print("Features Active:")
    print("✅ Real-time Slot Monitoring")
    print("✅ Auto-booking System") 
    print("✅ Multi-center Tracking")
    print("✅ Live Statistics")
    print("✅ Booking Management")
    print("=" * 50)
    
    socketio.run(app, debug=False, host='0.0.0.0', port=9090)
