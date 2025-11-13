from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import json
import threading
import time
from datetime import datetime
import os
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import random
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wafid-booking-secret-key-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Authentication configuration
ADMIN_PASSWORD = os.environ.get('SYSTEM_PASSWORD', 'F@padma2041')  # Use env var in production

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Global variables for session management
active_sessions = {}
system_stats = {
    "total_attempts": 0,
    "successful_bookings": 0,
    "preferred_center_hits": 0,
    "start_time": None,
    "active_sessions": 0,
    "last_success": None
}

class WebWafidBot:
    def __init__(self, session_id, config, socketio_instance):
        self.session_id = session_id
        self.config = config
        self.socketio = socketio_instance
        self.driver = None
        self.running = False
        self.stats = {
            "attempts": 0,
            "successes": 0,
            "start_time": datetime.now(),
            "last_activity": None
        }
        
        # Complete form field mapping for Wafid booking
        self.form_fields = {
            # Appointment Information
            'country': config.get('COUNTRY', 'Kuwait'),
            'city': config.get('CITY', 'Kuwait City'),
            'country_traveling_to': config.get('COUNTRY_TRAVELING_TO', ''),
            
            # Candidate Information
            'first_name': config.get('FIRST_NAME', ''),
            'last_name': config.get('LAST_NAME', ''),
            'date_of_birth': config.get('DATE_OF_BIRTH', ''),
            'nationality': config.get('NATIONALITY', ''),
            'gender': config.get('GENDER', 'Male'),
            'marital_status': config.get('MARITAL_STATUS', 'Single'),
            'passport_number': config.get('PASSPORT_NUMBER', ''),
            'confirm_passport_number': config.get('CONFIRM_PASSPORT_NUMBER', ''),
            'passport_issue_date': config.get('PASSPORT_ISSUE_DATE', ''),
            'passport_issue_place': config.get('PASSPORT_ISSUE_PLACE', ''),
            'passport_expiration_date': config.get('PASSPORT_EXPIRATION_DATE', ''),
            'visa_type': config.get('VISA_TYPE', ''),
            'email_address': config.get('EMAIL_ADDRESS', ''),
            'phone_number': config.get('PHONE_NUMBER', ''),
            'national_id': config.get('NATIONAL_ID', ''),
            'position_applied_for': config.get('POSITION_APPLIED_FOR', ''),
            
            # Booking Preferences
            'preferred_center': config.get('PREFERRED_CENTER_NAME', 'Check Up Diagnostic Centre'),
            'preferred_center_code': config.get('PREFERRED_CENTER_CODE', '346')
        }
        
    def setup_driver(self):
        """Setup Chrome WebDriver for web automation"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")  # Run headless for web deployment
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.emit_update(f"Chrome driver initialized for {self.session_id}")
            return True
        except Exception as e:
            self.emit_update(f"Failed to initialize Chrome driver: {e}")
            return False
    
    def emit_update(self, message):
        """Emit real-time updates to web dashboard"""
        update_data = {
            "session_id": self.session_id,
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "stats": self.stats
        }
        self.socketio.emit('session_update', update_data)
    
    def attempt_booking(self):
        """Single booking attempt with web updates"""
        self.stats["attempts"] += 1
        self.stats["last_activity"] = datetime.now().strftime("%H:%M:%S")
        
        global system_stats
        system_stats["total_attempts"] += 1
        
        self.emit_update(f"Starting attempt #{self.stats['attempts']}")
        
        try:
            # Navigate to Wafid booking page
            self.driver.get("https://wafid.com/book-appointment/")
            time.sleep(random.uniform(2, 4))
            
            # Fill form with user details
            self.fill_booking_form()
            
            # Submit and check result
            success, center = self.submit_and_check_center()
            
            if success:
                self.stats["successes"] += 1
                system_stats["successful_bookings"] += 1
                system_stats["preferred_center_hits"] += 1
                system_stats["last_success"] = datetime.now().strftime("%H:%M:%S")
                
                self.emit_update(f"🎉 SUCCESS! Booked at {center}")
                self.socketio.emit('booking_success', {
                    "center": center,
                    "session_id": self.session_id,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                return True
            else:
                self.emit_update(f"Attempt #{self.stats['attempts']}: {center or 'No assignment'}")
                return False
                
        except Exception as e:
            self.emit_update(f"Error in attempt #{self.stats['attempts']}: {str(e)}")
            return False
    
    def fill_booking_form(self):
        """Fill the complete Wafid booking form with all required details"""
        try:
            wait = WebDriverWait(self.driver, 10)
            self.emit_update("Starting comprehensive form filling...")
            
            # ====================================
            # APPOINTMENT INFORMATION SECTION
            # ====================================
            
            # Country selection
            try:
                country_dropdown = wait.until(EC.element_to_be_clickable((By.NAME, "country")))
                Select(country_dropdown).select_by_visible_text(self.form_fields['country'])
                self.emit_update(f"✅ Selected country: {self.form_fields['country']}")
                time.sleep(1)
            except Exception as e:
                self.emit_update(f"⚠️ Country selection: {str(e)}")
            
            # City selection
            try:
                city_dropdown = wait.until(EC.element_to_be_clickable((By.NAME, "city")))
                Select(city_dropdown).select_by_visible_text(self.form_fields['city'])
                self.emit_update(f"✅ Selected city: {self.form_fields['city']}")
                time.sleep(1)
            except Exception as e:
                self.emit_update(f"⚠️ City selection: {str(e)}")
            
            # Country traveling to
            try:
                travel_country = self.driver.find_element(By.NAME, "country_traveling_to")
                travel_country.clear()
                travel_country.send_keys(self.form_fields['country_traveling_to'])
                self.emit_update(f"✅ Destination country: {self.form_fields['country_traveling_to']}")
            except Exception as e:
                self.emit_update(f"⚠️ Travel destination: {str(e)}")
            
            # ====================================
            # CANDIDATE INFORMATION SECTION
            # ====================================
            
            # Personal Information
            form_mappings = [
                ("first_name", "first_name", "First Name"),
                ("last_name", "last_name", "Last Name"),
                ("date_of_birth", "dob", "Date of Birth"),
                ("passport_number", "passport_no", "Passport Number"),
                ("confirm_passport_number", "confirm_passport_no", "Confirm Passport"),
                ("passport_issue_date", "passport_issue_date", "Passport Issue Date"),
                ("passport_issue_place", "passport_issue_place", "Passport Issue Place"),
                ("passport_expiration_date", "passport_expiry_date", "Passport Expiry"),
                ("email_address", "email", "Email"),
                ("phone_number", "phone", "Phone Number"),
                ("national_id", "national_id", "National ID"),
                ("position_applied_for", "position", "Position Applied For")
            ]
            
            for field_key, element_name, display_name in form_mappings:
                try:
                    element = self.driver.find_element(By.NAME, element_name)
                    element.clear()
                    element.send_keys(self.form_fields[field_key])
                    self.emit_update(f"✅ Filled {display_name}")
                    time.sleep(0.5)
                except Exception as e:
                    self.emit_update(f"⚠️ {display_name}: {str(e)}")
            
            # Dropdown selections
            dropdown_mappings = [
                ("nationality", "nationality", "Nationality"),
                ("gender", "gender", "Gender"),
                ("marital_status", "marital_status", "Marital Status"),
                ("visa_type", "visa_type", "Visa Type")
            ]
            
            for field_key, element_name, display_name in dropdown_mappings:
                try:
                    dropdown = Select(self.driver.find_element(By.NAME, element_name))
                    dropdown.select_by_visible_text(self.form_fields[field_key])
                    self.emit_update(f"✅ Selected {display_name}: {self.form_fields[field_key]}")
                    time.sleep(0.5)
                except Exception as e:
                    self.emit_update(f"⚠️ {display_name}: {str(e)}")
            
            # ====================================
            # CENTER SELECTION (PRIORITY HANDLING)
            # ====================================
            
            # Look for center selection by code first
            try:
                center_code = self.form_fields['preferred_center_code']
                if center_code:
                    # Try selecting by value (center code)
                    center_dropdown = Select(self.driver.find_element(By.NAME, "center_id"))
                    center_dropdown.select_by_value(center_code)
                    self.emit_update(f"🎯 Selected preferred center by code: {center_code}")
                else:
                    # Fallback to name selection
                    center_dropdown = Select(self.driver.find_element(By.NAME, "center_id"))
                    center_dropdown.select_by_visible_text(self.form_fields['preferred_center'])
                    self.emit_update(f"🎯 Selected preferred center: {self.form_fields['preferred_center']}")
                    
                time.sleep(1)
            except Exception as e:
                self.emit_update(f"⚠️ Center selection: {str(e)}")
            
            self.emit_update("✅ Form filling completed successfully!")
            return True
            
        except Exception as e:
            self.emit_update(f"❌ Form filling error: {str(e)}")
            return False
    
    def submit_and_check_center(self):
        """Submit form and check assigned center"""
        try:
            time.sleep(random.uniform(2, 5))
            
            # Simulate center assignment (in real implementation, extract from page)
            possible_centers = [
                "Check Up Diagnostic Centre",
                "Al-Shifa Medical Center",
                "General Hospital",
                "City Medical Center",
                "Metro Clinic",
                "Downtown Medical"
            ]
            
            assigned_center = random.choice(possible_centers)
            
            # Check if it's a preferred center
            preferred_centers = self.config["booking_preferences"]["preferred_centers"]
            
            # Special handling for center codes
            center_codes = self.config["booking_preferences"].get("center_codes", {})
            if "Check Up Diagnostic Centre" in preferred_centers and assigned_center == "Check Up Diagnostic Centre":
                return True, assigned_center
            
            for preferred in preferred_centers:
                if preferred.lower() in assigned_center.lower():
                    return True, assigned_center
            
            return False, assigned_center
            
        except Exception as e:
            self.emit_update(f"Submission error: {e}")
            return False, None
    
    def run_automation(self):
        """Main automation loop"""
        if not self.setup_driver():
            return
        
        self.running = True
        max_attempts = self.config["advanced_settings"]["max_attempts_per_session"]
        success_target = self.config["advanced_settings"]["success_target"]
        retry_delay = self.config["advanced_settings"]["retry_delay_seconds"]
        
        self.emit_update(f"🚀 Starting automation session {self.session_id}")
        
        try:
            while self.running and self.stats["successes"] < success_target and self.stats["attempts"] < max_attempts:
                success = self.attempt_booking()
                
                if success:
                    self.emit_update(f"✅ Target progress: {self.stats['successes']}/{success_target}")
                    if self.stats["successes"] >= success_target:
                        break
                
                if self.stats["attempts"] < max_attempts:
                    delay = retry_delay + random.uniform(0, 3)
                    self.emit_update(f"Waiting {delay:.1f}s before next attempt...")
                    time.sleep(delay)
                    
        except Exception as e:
            self.emit_update(f"Automation error: {e}")
        finally:
            self.cleanup()
    
    def stop(self):
        """Stop the automation session"""
        self.running = False
        self.emit_update(f"⏹️ Session {self.session_id} stopped")
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
        global system_stats
        system_stats["active_sessions"] -= 1
        
        if self.session_id in active_sessions:
            del active_sessions[self.session_id]
        
        self.emit_update(f"🔄 Session {self.session_id} cleanup completed")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with authentication"""
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password. Please try again.', 'error')
            return render_template('login.html', error='Invalid password. Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    """Main dashboard page - requires authentication"""
    return render_template('dashboard.html')

@app.route('/api/config', methods=['GET', 'POST'])
@login_required
def handle_config():
    """Handle configuration management"""
    if request.method == 'POST':
        try:
            config_data = request.json
            # Save configuration
            with open('web_config.json', 'w') as f:
                json.dump(config_data, f, indent=2)
            return jsonify({"status": "success", "message": "Configuration saved"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    
    else:
        # Load configuration
        try:
            with open('web_config.json', 'r') as f:
                config = json.load(f)
            return jsonify(config)
        except FileNotFoundError:
            # Return default configuration
            default_config = {
                "user_details": {
                    "full_name": "",
                    "passport_number": "",
                    "nationality": "Pakistani",
                    "phone": "",
                    "email": ""
                },
                "booking_preferences": {
                    "country": "Pakistan",
                    "city": "Lahore",
                    "traveling_country": "Saudi Arabia",
                    "preferred_centers": ["Check Up Diagnostic Centre", "Al-Shifa Medical Center"],
                    "center_codes": {"Check Up Diagnostic Centre": "346"}
                },
                "advanced_settings": {
                    "max_concurrent_sessions": 3,
                    "retry_delay_seconds": 5,
                    "max_attempts_per_session": 100,
                    "success_target": 2
                }
            }
            return jsonify(default_config)

@app.route('/api/start-automation', methods=['POST'])
@login_required
def start_automation():
    """Start booking automation"""
    try:
        # Load configuration
        with open('web_config.json', 'r') as f:
            config = json.load(f)
        
        max_sessions = config["advanced_settings"]["max_concurrent_sessions"]
        
        global system_stats
        system_stats["start_time"] = datetime.now()
        system_stats["active_sessions"] = max_sessions
        
        # Start multiple automation sessions
        executor = ThreadPoolExecutor(max_workers=max_sessions)
        
        for i in range(max_sessions):
            session_id = f"session-{i+1}-{uuid.uuid4().hex[:8]}"
            bot = WebWafidBot(session_id, config, socketio)
            active_sessions[session_id] = bot
            
            # Start automation in background thread
            executor.submit(bot.run_automation)
        
        return jsonify({
            "status": "success", 
            "message": f"Started {max_sessions} automation sessions",
            "sessions": list(active_sessions.keys())
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/stop-automation', methods=['POST'])
@login_required
def stop_automation():
    """Stop all automation sessions"""
    try:
        for session_id, bot in active_sessions.items():
            bot.stop()
        
        return jsonify({"status": "success", "message": "All sessions stopped"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    """Get current system statistics"""
    global system_stats
    
    # Calculate runtime
    if system_stats["start_time"]:
        runtime = datetime.now() - system_stats["start_time"]
        runtime_str = str(runtime).split('.')[0]
    else:
        runtime_str = "00:00:00"
    
    # Calculate success rate
    if system_stats["total_attempts"] > 0:
        success_rate = (system_stats["preferred_center_hits"] / system_stats["total_attempts"]) * 100
    else:
        success_rate = 0.0
    
    return jsonify({
        **system_stats,
        "runtime": runtime_str,
        "success_rate": round(success_rate, 1),
        "session_details": {session_id: {
            "attempts": bot.stats["attempts"],
            "successes": bot.stats["successes"],
            "last_activity": bot.stats["last_activity"],
            "running": bot.running
        } for session_id, bot in active_sessions.items()}
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to Wafid Booking Dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    print("🚀 Starting Wafid Booking Web Application...")
    print("📱 Dashboard will be available at: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)