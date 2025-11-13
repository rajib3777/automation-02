"""
Enhanced Wafid Booking Bot with Advanced Monitoring and Backup Strategies
Maximum success rate through intelligent retry logic and fallback mechanisms
"""

from flask import Flask, render_template, request, jsonify, session
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

# Import our enhanced modules
from enhanced_monitoring import EnhancedMonitor, FailureType
from backup_strategies import BackupStrategies, BrowserType, FormFillStrategy
from center_manager import CenterManager, PreferredCenter, CenterStatus

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wafid-booking-enhanced-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for session management
active_sessions = {}
system_stats = {
    "total_attempts": 0,
    "successful_bookings": 0,
    "preferred_center_hits": 0,
    "start_time": None,
    "active_sessions": 0,
    "last_success": None,
    "enhanced_features_active": True
}

class EnhancedWebWafidBot:
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
            "last_activity": None,
            "retries_used": 0,
            "fallback_strategies_used": 0,
            "centers_attempted": 0,
            "successful_center": None
        }
        
        # Initialize enhanced monitoring, backup systems, and center management
        self.monitor = EnhancedMonitor(socketio_instance)
        self.backup_strategies = BackupStrategies(socketio_instance)
        self.center_manager = CenterManager(socketio_instance)
        
        # Complete form field mapping for Wafid booking
        self.form_fields = {
            # Appointment Information
            'country': config.get('COUNTRY', 'Kuwait'),
            'city': config.get('CITY', 'Kuwait City'),
            'country_traveling_to': config.get('COUNTRY_TRAVELING_TO', 'Kuwait'),
            
            # Candidate Information
            'first_name': config.get('FIRST_NAME', ''),
            'last_name': config.get('LAST_NAME', ''),
            'date_of_birth': config.get('DATE_OF_BIRTH', ''),
            'nationality': config.get('NATIONALITY', ''),
            'gender': config.get('GENDER', 'Male'),
            'marital_status': config.get('MARITAL_STATUS', 'Single'),
            'passport_number': config.get('PASSPORT_NUMBER', ''),
            'passport_confirm': config.get('PASSPORT_NUMBER', ''),
            'passport_issue_date': config.get('PASSPORT_ISSUE_DATE', ''),
            'passport_issue_place': config.get('PASSPORT_ISSUE_PLACE', ''),
            'passport_expiration_date': config.get('PASSPORT_EXPIRATION_DATE', ''),
            'visa_type': config.get('VISA_TYPE', 'Work Visa'),
            'email_address': config.get('EMAIL_ADDRESS', ''),
            'phone_no': config.get('PHONE_NO', ''),
            'national_id': config.get('NATIONAL_ID', ''),
            'position_applied_for': config.get('POSITION_APPLIED_FOR', '')
        }
    
    def setup_driver(self, browser_config=None):
        """Setup WebDriver with enhanced configurations"""
        try:
            if browser_config:
                self.driver = self.backup_strategies.create_driver_with_config(browser_config)
                self.backup_strategies.apply_network_resilience(self.driver)
            else:
                # Default Chrome setup
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                self.driver = webdriver.Chrome(options=options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
            
        except Exception as e:
            self.emit_update(f"❌ Driver setup failed: {str(e)}", "error")
            return False
    
    def emit_update(self, message, level="info"):
        """Emit real-time updates to web dashboard"""
        update_data = {
            "session_id": self.session_id,
            "message": message,
            "level": level,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "stats": self.stats
        }
        self.socketio.emit('session_update', update_data)
    
    def enhanced_booking_attempt(self):
        """Enhanced booking attempt with center targeting and monitoring"""
        self.stats["attempts"] += 1
        self.stats["last_activity"] = datetime.now().strftime("%H:%M:%S")
        
        global system_stats
        system_stats["total_attempts"] += 1
        
        # Get center targeting strategy
        center_strategy = self.center_manager.get_center_targeting_strategy()
        if not center_strategy:
            self.emit_update("❌ No available centers to target", "error")
            return False
        
        target_center = center_strategy["target_center"]
        max_attempts_for_center = center_strategy["max_attempts"]
        
        self.emit_update(f"🎯 Targeting: {target_center} (Priority {center_strategy['priority']})")
        
        # Check website health before starting
        if not self.monitor.check_website_health():
            self.emit_update("⚠️ Website health check failed - delaying attempt", "warning")
            time.sleep(30)  # Wait before retrying
        
        attempt_start_time = time.time()
        current_attempt = 0
        consecutive_center_failures = 0
        
        while current_attempt < 5:  # Maximum 5 total attempts
            try:
                current_attempt += 1
                self.emit_update(f"🚀 Enhanced attempt #{current_attempt} for {target_center}")
                
                # Try different browser configurations
                if current_attempt == 1:
                    browser_config = None  # Use default
                else:
                    browser_config = self.backup_strategies.get_next_browser_config()
                    self.emit_update(f"🔄 Switching to {browser_config.browser_type.value} configuration")
                    self.stats["fallback_strategies_used"] += 1
                
                # Setup driver with current configuration
                if not self.setup_driver(browser_config):
                    continue
                
                # Navigate to Wafid booking page
                self.driver.get("https://wafid.com/book-appointment/")
                time.sleep(random.uniform(2, 4))
                
                # Check for CAPTCHA
                captcha_detected, captcha_msg = self.backup_strategies.detect_and_handle_captcha(self.driver)
                if captcha_detected:
                    result = self.monitor.record_attempt(
                        success=False, 
                        error=Exception(captcha_msg),
                        response_time=time.time() - attempt_start_time,
                        page_source=self.driver.page_source
                    )
                    self.emit_update("🤖 CAPTCHA detected - manual intervention required", "warning")
                    return False
                
                # Try different form filling strategies
                form_strategy = self.backup_strategies.get_next_form_strategy()
                form_success = self.backup_strategies.fill_form_with_strategy(
                    self.driver, self.form_fields, form_strategy
                )
                
                if not form_success:
                    # Try next strategy
                    self.emit_update("📝 Form filling failed, trying alternative method")
                    continue
                
                # Add center preference to form (if applicable)
                self.apply_center_preference(target_center)
                
                # Submit and check result
                success, assigned_center = self.submit_and_check_center_enhanced()
                
                if success:
                    # Validate center assignment
                    center_validated, center_msg = self.center_manager.validate_center_assignment(
                        self.driver.page_source, target_center
                    )
                    
                    # Record center attempt result
                    response_time = time.time() - attempt_start_time
                    self.center_manager.record_center_attempt(target_center, True, response_time)
                    
                    # Validate the booking success
                    validated, validation_msg = self.monitor.validate_booking_success(self.driver, assigned_center)
                    
                    if validated:
                        result = self.monitor.record_attempt(
                            success=True,
                            response_time=response_time,
                            center=assigned_center
                        )
                        
                        self.stats["successes"] += 1
                        self.stats["successful_center"] = assigned_center
                        self.stats["centers_attempted"] += 1
                        system_stats["successful_bookings"] += 1
                        system_stats["preferred_center_hits"] += 1
                        system_stats["last_success"] = datetime.now().strftime("%H:%M:%S")
                        
                        # Update browser config success rate
                        if browser_config:
                            self.backup_strategies.update_config_success_rate(browser_config, True)
                        
                        success_msg = f"🎉 BOOKING SUCCESS at {assigned_center}!"
                        if center_validated:
                            success_msg += f" ✅ {center_msg}"
                        else:
                            success_msg += f" ⚠️ {center_msg}"
                        
                        self.emit_update(success_msg, "success")
                        self.socketio.emit('booking_success', {
                            "center": assigned_center,
                            "target_center": target_center,
                            "center_validated": center_validated,
                            "session_id": self.session_id,
                            "validation": validation_msg,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "attempts_used": current_attempt,
                            "strategies_used": self.stats["fallback_strategies_used"],
                            "centers_attempted": self.stats["centers_attempted"]
                        })
                        return True
                    else:
                        self.emit_update(f"⚠️ Booking validation failed: {validation_msg}", "warning")
                        continue
                else:
                    # Record failed attempt for this center
                    response_time = time.time() - attempt_start_time
                    self.center_manager.record_center_attempt(target_center, False, response_time)
                    consecutive_center_failures += 1
                    
                    self.emit_update(f"❌ Attempt #{current_attempt} at {target_center}: {assigned_center or 'No assignment'}")
                    
                    # Check if we should switch centers
                    if self.center_manager.should_switch_center(target_center, consecutive_center_failures):
                        # Try to get next center
                        excluded_centers = [target_center]  # Exclude current failing center
                        next_center_strategy = self.center_manager.get_center_targeting_strategy()
                        
                        if next_center_strategy and next_center_strategy["target_center"] != target_center:
                            target_center = next_center_strategy["target_center"]
                            consecutive_center_failures = 0
                            self.stats["centers_attempted"] += 1
                            self.emit_update(f"🔄 Switched to new target: {target_center}")
                        else:
                            self.emit_update("❌ No more centers available to try", "error")
                            break
                
                # Determine if we should retry
                last_failure = FailureType.NO_SLOTS_AVAILABLE if not success else None
                should_retry, delay = self.monitor.should_retry(current_attempt, last_failure)
                
                if should_retry and current_attempt < 5:
                    self.stats["retries_used"] += 1
                    self.emit_update(f"⏳ Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    break
                    
            except Exception as e:
                response_time = time.time() - attempt_start_time
                result = self.monitor.record_attempt(
                    success=False,
                    error=e,
                    response_time=response_time,
                    page_source=getattr(self.driver, 'page_source', '')
                )
                
                # Record failed center attempt
                self.center_manager.record_center_attempt(target_center, False, response_time)
                consecutive_center_failures += 1
                
                # Update browser config success rate
                if browser_config:
                    self.backup_strategies.update_config_success_rate(browser_config, False)
                
                failure_type = result.failure_type
                self.emit_update(f"❌ Error at {target_center} ({failure_type.value}): {str(e)}", "error")
                
                # Determine if we should retry
                should_retry, delay = self.monitor.should_retry(current_attempt, failure_type)
                
                if should_retry and current_attempt < 5:
                    self.stats["retries_used"] += 1
                    self.emit_update(f"🔄 Retrying with different strategy in {delay} seconds...")
                    time.sleep(delay)
                else:
                    break
            
            finally:
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = None
        
        # Record final failure if all attempts exhausted
        if current_attempt >= 5:
            self.emit_update(f"❌ All {current_attempt} attempts exhausted for available centers", "error")
        
        return False
    
    def apply_center_preference(self, target_center: str):
        """Apply center preference to form if center selection is available"""
        try:
            # Look for center selection dropdown or field
            center_selectors = [
                "select[name*='center']",
                "select[name*='location']",
                "select[name*='office']",
                "select[id*='center']",
                "select[id*='location']"
            ]
            
            for selector in center_selectors:
                try:
                    center_dropdown = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    # Try to find and select the target center
                    options = center_dropdown.find_elements(By.TAG_NAME, "option")
                    for option in options:
                        option_text = option.text.lower()
                        target_lower = target_center.lower()
                        
                        # Check for exact match or partial match
                        if (target_lower in option_text or 
                            option_text in target_lower or
                            any(word in option_text for word in target_lower.split())):
                            
                            option.click()
                            self.emit_update(f"✅ Selected preferred center: {option.text}")
                            time.sleep(1)
                            return True
                            
                except Exception:
                    continue
            
            # If no dropdown found, log that center preference couldn't be applied
            self.emit_update(f"ℹ️ No center selection field found - using default assignment")
            return False
            
        except Exception as e:
            self.emit_update(f"⚠️ Could not apply center preference: {str(e)}")
            return False
    
    def submit_and_check_center_enhanced(self):
        """Enhanced submission with better error handling"""
        try:
            # Find and click submit button
            submit_selectors = [
                "input[type='submit']",
                "button[type='submit']",
                ".submit-btn",
                "#submit-appointment",
                "button:contains('Submit')",
                "input[value*='Submit']"
            ]
            
            submit_clicked = False
            for selector in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_btn.is_enabled():
                        submit_btn.click()
                        submit_clicked = True
                        break
                except:
                    continue
            
            if not submit_clicked:
                # Try JavaScript submission as fallback
                self.driver.execute_script("document.forms[0].submit();")
            
            # Wait for response
            time.sleep(random.uniform(3, 6))
            
            # Check for success indicators
            page_source = self.driver.page_source.lower()
            
            # Success indicators
            success_keywords = [
                "appointment confirmed",
                "booking successful",
                "appointment scheduled",
                "confirmation number",
                "reference number"
            ]
            
            for keyword in success_keywords:
                if keyword in page_source:
                    # Try to extract center name
                    center = self.extract_center_name(self.driver.page_source)
                    return True, center or "Appointment Center"
            
            # Check for specific failure messages
            failure_keywords = [
                "no slots available",
                "fully booked",
                "appointment not available",
                "try again later"
            ]
            
            for keyword in failure_keywords:
                if keyword in page_source:
                    return False, f"No slots available ({keyword})"
            
            return False, "Unknown response"
            
        except Exception as e:
            return False, f"Submission error: {str(e)}"
    
    def extract_center_name(self, page_source):
        """Extract center name from confirmation page"""
        try:
            # Common patterns for center names
            import re
            
            patterns = [
                r"center[:\s]+([A-Za-z\s]+)",
                r"location[:\s]+([A-Za-z\s]+)",
                r"appointment at[:\s]+([A-Za-z\s]+)",
                r"office[:\s]+([A-Za-z\s]+)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, page_source, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            return None
            
        except Exception:
            return None
    
    def run_enhanced_session(self):
        """Run enhanced booking session with monitoring"""
        self.running = True
        self.emit_update("🚀 Starting enhanced booking session with monitoring")
        
        try:
            while self.running:
                success = self.enhanced_booking_attempt()
                
                if success:
                    self.emit_update("✅ Session completed successfully!")
                    break
                
                # Smart delay based on monitoring data
                if self.monitor.health_status.consecutive_failures > 3:
                    delay = random.uniform(30, 60)  # Longer delay if many failures
                    self.emit_update(f"⏸️ Extended delay ({delay:.0f}s) due to consecutive failures")
                else:
                    delay = random.uniform(10, 20)  # Normal delay
                
                time.sleep(delay)
                
        except Exception as e:
            self.emit_update(f"❌ Session error: {str(e)}", "error")
        finally:
            self.running = False
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass

# Flask Routes (keeping existing routes and adding new monitoring endpoints)

@app.route('/')
def dashboard():
    """Enhanced dashboard with monitoring features"""
    return render_template('enhanced_dashboard.html')

@app.route('/start_session', methods=['POST'])
def start_session():
    """Start enhanced booking session"""
    try:
        data = request.json
        session_id = str(uuid.uuid4())[:8]
        
        # Create enhanced bot instance
        bot = EnhancedWebWafidBot(session_id, data, socketio)
        active_sessions[session_id] = bot
        
        # Start session in background thread
        thread = threading.Thread(target=bot.run_enhanced_session)
        thread.daemon = True
        thread.start()
        
        global system_stats
        system_stats["active_sessions"] = len(active_sessions)
        if system_stats["start_time"] is None:
            system_stats["start_time"] = datetime.now().strftime("%H:%M:%S")
        
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "message": "Enhanced booking session started with monitoring"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/stop_session', methods=['POST'])
def stop_session():
    """Stop booking session"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id in active_sessions:
            active_sessions[session_id].running = False
            del active_sessions[session_id]
            
            global system_stats
            system_stats["active_sessions"] = len(active_sessions)
            
            return jsonify({"status": "success", "message": "Session stopped"})
        else:
            return jsonify({"status": "error", "message": "Session not found"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/system_stats')
def get_system_stats():
    """Get enhanced system statistics"""
    try:
        # Get monitoring stats from active sessions
        total_monitor_stats = {
            "total_attempts": 0,
            "successful_attempts": 0,
            "retry_success_rate": 0.0,
            "average_response_time": 0.0
        }
        
        failure_analysis = {}
        backup_summary = {}
        center_analytics = {}
        
        for session_id, bot in active_sessions.items():
            monitor_stats = bot.monitor.get_stats_summary()
            total_monitor_stats["total_attempts"] += bot.monitor.stats["total_attempts"]
            total_monitor_stats["successful_attempts"] += bot.monitor.stats["successful_attempts"]
            
            # Get failure analysis from first active session
            if not failure_analysis:
                failure_analysis = bot.monitor.get_failure_analysis()
                backup_summary = bot.backup_strategies.get_backup_summary()
                center_analytics = bot.center_manager.get_center_analytics()
        
        # Calculate overall success rate
        if total_monitor_stats["total_attempts"] > 0:
            total_monitor_stats["retry_success_rate"] = (
                total_monitor_stats["successful_attempts"] / 
                total_monitor_stats["total_attempts"] * 100
            )
        
        enhanced_stats = {
            **system_stats,
            "monitoring": total_monitor_stats,
            "failure_analysis": failure_analysis,
            "backup_strategies": backup_summary,
            "center_analytics": center_analytics,
            "enhanced_features": {
                "intelligent_retries": True,
                "multiple_browsers": True,
                "form_strategies": True,
                "health_monitoring": True,
                "success_validation": True,
                "center_targeting": True
            }
        }
        
        return jsonify(enhanced_stats)
        
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/center_stats')
def get_center_stats():
    """Get detailed center statistics and performance"""
    try:
        center_data = {
            "preferred_centers": [
                "Precision Diagnostics Ltd",
                "Mediquest Diagnostics Ltd", 
                "Allied Diagnostics Ltd"
            ],
            "center_performance": {},
            "current_target": None
        }
        
        # Get center data from active sessions
        for session_id, bot in active_sessions.items():
            center_analytics = bot.center_manager.get_center_analytics()
            center_status = bot.center_manager.get_centers_status_summary()
            
            center_data["center_performance"] = center_analytics.get("center_performance", [])
            center_data["current_target"] = center_analytics.get("successful_center")
            center_data["center_status"] = center_status
            break  # Use data from first active session
        
        return jsonify(center_data)
        
    except Exception as e:
        return jsonify({"error": str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to enhanced Wafid booking system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)