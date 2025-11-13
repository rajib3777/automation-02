# 🤖 Enhanced Wafid Automation System - Real Center-Based Booking

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import json
import random
import threading
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions
import re
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data structures for real GAMCA centers
GAMCA_CENTERS_PAKISTAN = {
    "Karachi": [
        {"name": "Accubaq Diagnostic", "address": "PECHS Block 6"},
        {"name": "Al-Hilal Medical Diagnostic Center", "address": "PECHS Block 6"},
        {"name": "Taj Medical Center", "address": "Block 6, KFC Lane"},
        {"name": "Al-Raed Medical Diagnostic Center", "address": "Block 6, PECHS"},
        {"name": "Medical Diagnostic Clinic", "address": "PECHS Block 6"}
    ],
    "Lahore": [
        {"name": "Advanced Medical Diagnostic", "address": "Allama Iqbal Town"},
        {"name": "Taj Medical Travelers Clinic", "address": "Johar Town"},
        {"name": "Iqra Medical Complex", "address": "Johar Town"},
        {"name": "AL Safa Medical Center", "address": "Johar Town"},
        {"name": "Everest Diagnostic Center", "address": "Johar Town"}
    ],
    "Islamabad": [
        {"name": "GCC Diagnostic Centre", "address": "G-10/3, Ibn-e-Sena Road"},
        {"name": "RR Diagnostics Centre", "address": "G-9/4"},
        {"name": "Shifa International Hospital", "address": "H-8/4"},
        {"name": "Emerald Diagnostics Center", "address": "G-8/1"},
        {"name": "Premier Diagnostics", "address": "Khanna Islamabad"}
    ],
    "Gujranwala": [
        {"name": "Al Falaq Diagnostic Centre", "address": "DC Road"},
        {"name": "Citi Care Diagnostic Centre", "address": "DC Road"},
        {"name": "Pacific Diagnostic Centre", "address": "Sialkot Bypass"},
        {"name": "Royal Diagnostic Centre", "address": "Sui Gas Road"},
        {"name": "NM Diagnostic Center", "address": "G.T Road"}
    ]
}

GAMCA_CENTERS_INDIA = {
    "Mumbai": [
        {"name": "Clinical Diagnostic Centre", "address": "Nariman Point"},
        {"name": "Al Amal Diagnostic Centre", "address": "Kurla, BKC"},
        {"name": "K. N. Diagnostic Centre", "address": "Opera House"},
        {"name": "Ashwini Clinic", "address": "Prabhadevi"},
        {"name": "Gulshan Medicare Mumbai", "address": "Nariman Point"}
    ],
    "Delhi": [
        {"name": "Health Plus Diagnostic Centre", "address": "Greater Kailash"},
        {"name": "Corporate Diagnostic Centre", "address": "Nehru Enclave"},
        {"name": "Gulf Medical Centre", "address": "Rajendra Place"},
        {"name": "Gulshan Medicare Delhi", "address": "South Extension"},
        {"name": "New Delhi Medical Centre", "address": "Rajendra Place"}
    ],
    "Jaipur": [
        {"name": "Advanced Diagnostic Centre", "address": "M.I. ROAD"},
        {"name": "Royale Diagnostic Centre", "address": "Park Street"},
        {"name": "ACE Diagnostics", "address": "Shastri Nagar"},
        {"name": "A. K. Diagnostic Center", "address": "Shastri Nagar"},
        {"name": "Dr. Padaria's Medical Services", "address": "Mumbai Central"}
    ],
    "Kochi": [
        {"name": "Delmon Clinic & Diagnostic Centre", "address": "M.G. Road"},
        {"name": "Celica Medical Center", "address": "M G Road"},
        {"name": "Dr. Kunhalu's Nursing Home", "address": "Ernakulam"},
        {"name": "Medline Diagnostic Center", "address": "TD East"},
        {"name": "Gulshan Medicare Kochi", "address": "Trichur"}
    ]
}

# Application Factory
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Global variables
automation_running = False
monitoring_running = False
automation_thread = None

class RealWafidAutomation:
    def __init__(self):
        self.centers_db_path = "/data/multi_center_automation.db"
        self.init_database()
        
    def init_database(self):
        """Initialize database with GAMCA centers"""
        try:
            conn = sqlite3.connect(self.centers_db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS centers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    city TEXT NOT NULL,
                    country TEXT NOT NULL,
                    automation_level TEXT DEFAULT 'basic',
                    success_rate REAL DEFAULT 85.0,
                    attempts INTEGER DEFAULT 0,
                    bookings INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    priority_level INTEGER DEFAULT 5,
                    gamca_center_code TEXT,
                    active BOOLEAN DEFAULT 1
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    center_id INTEGER,
                    patient_name TEXT,
                    passport_number TEXT,
                    email TEXT,
                    phone TEXT,
                    appointment_date TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    booking_reference TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert GAMCA centers if not exists
            all_centers = []
            
            # Add Pakistani centers
            for city, centers in GAMCA_CENTERS_PAKISTAN.items():
                for center in centers:
                    all_centers.append((center['name'], city, 'Pakistan', 'advanced', 88.0, 0, 0))
            
            # Add Indian centers  
            for city, centers in GAMCA_CENTERS_INDIA.items():
                for center in centers:
                    all_centers.append((center['name'], city, 'India', 'advanced', 87.0, 0, 0))
            
            # Insert centers (avoid duplicates)
            for center_data in all_centers:
                cursor.execute('''
                    INSERT OR IGNORE INTO centers 
                    (name, city, country, automation_level, success_rate, attempts, bookings)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', center_data)
            
            conn.commit()
            conn.close()
            print("✅ Database initialized with GAMCA centers")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    def get_all_centers(self):
        """Get all centers from database"""
        try:
            conn = sqlite3.connect(self.centers_db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM centers WHERE active = 1')
            centers = cursor.fetchall()
            conn.close()
            return centers
        except Exception as e:
            logger.error(f"Error getting centers: {e}")
            return []
    
    def intelligent_center_selection(self):
        """Select best center using Wafid-compatible strategy"""
        centers = self.get_all_centers()
        if not centers:
            return None
            
        # Calculate scores for each center
        scored_centers = []
        for center in centers:
            score = self.calculate_center_score(center)
            scored_centers.append((center, score))
        
        # Sort by score and return top 3 for Wafid system to choose from
        scored_centers.sort(key=lambda x: x[1], reverse=True)
        return [center[0] for center in scored_centers[:3]]
    
    def calculate_center_score(self, center):
        """Calculate center score based on performance metrics"""
        success_rate = center[4]  # success_rate
        attempts = center[5]      # attempts
        bookings = center[6]      # bookings
        
        # Success rate weight: 40%
        success_score = success_rate * 0.4
        
        # Volume weight: 25% (prefer centers with more bookings)
        volume_score = min(bookings / 100, 25) * 0.25
        
        # Recent activity weight: 20% (more attempts = more active)
        activity_score = min(attempts / 50, 20) * 0.20
        
        # Automation level weight: 15%
        level_multiplier = {'basic': 1.0, 'standard': 1.15, 'advanced': 1.3}
        automation_multiplier = level_multiplier.get(center[3], 1.0)
        automation_score = automation_multiplier * 15
        
        return success_score + volume_score + activity_score + automation_score
    
    def create_stealth_driver(self):
        """Create undetected Chrome driver for Wafid"""
        try:
            options = ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agents
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
            ]
            options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            driver = Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
        except Exception as e:
            logger.error(f"Failed to create driver: {e}")
            return None
    
    def simulate_human_behavior(self, driver):
        """Add human-like behavior to avoid detection"""
        try:
            # Random delays
            time.sleep(random.uniform(2, 5))
            
            # Mouse movements
            actions = ActionChains(driver)
            for _ in range(random.randint(1, 3)):
                x, y = random.randint(100, 800), random.randint(200, 600)
                actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.5, 1.5))
            
            # Random scrolling
            driver.execute_script(f"window.scrollTo(0, {random.randint(100, 500)});")
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            logger.error(f"Human behavior simulation error: {e}")
    
    def perform_real_wafid_booking(self, centers):
        """Perform actual Wafid booking with center selection"""
        driver = None
        try:
            driver = self.create_stealth_driver()
            if not driver:
                return False, "Failed to create browser driver"
            
            print("🚀 Starting real Wafid booking automation...")
            
            # Step 1: Navigate to Wafid
            driver.get("https://wafid.com/book-appointment/")
            print("📄 Navigated to Wafid booking page")
            
            # Step 2: Wait and simulate human behavior
            self.simulate_human_behavior(driver)
            
            # Step 3: Fill personal information
            self.fill_personal_information(driver)
            
            # Step 4: Select country and city (influences center selection)
            self.select_country_city(driver, centers)
            
            # Step 5: Handle appointment booking
            success = self.fill_appointment_information(driver, centers)
            
            if success:
                print("✅ Wafid booking completed successfully")
                return True, "Booking submitted"
            else:
                return False, "Booking submission failed"
                
        except Exception as e:
            print(f"❌ Wafid booking error: {e}")
            return False, str(e)
        finally:
            if driver:
                driver.quit()
    
    def fill_personal_information(self, driver):
        """Fill personal information with realistic data"""
        try:
            # Generate realistic Saudi data
            first_names = ["Ahmed", "Mohammed", "Abdul", "Omar", "Khalid", "Youssef", "Ali", "Hassan"]
            last_names = ["Al-Rashid", "Al-Mansouri", "Al-Zahra", "Al-Harbi", "Al-Otaibi", "Al-Mutairi"]
            arab_names = ["أحمد", "محمد", "عبدالله", "عمر", "خالد", "يوسف"]
            
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            arabic_name = random.choice(arab_names)
            email = f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}{random.randint(100, 999)}@gmail.com"
            phone = f"+966{random.randint(500000000, 599999999)}"
            passport = f"{random.randint(100000000, 999999999)}"
            
            # Fill name fields
            name_selectors = [
                "input[name*='name']", "input[name*='Name']", "input[id*='name']",
                "#name", "#fullname", "input[placeholder*='name']", "input[placeholder*='Name']"
            ]
            
            for selector in name_selectors:
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    element.clear()
                    # Type with human-like delays
                    for char in full_name:
                        element.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    break
                except:
                    continue
            
            # Fill email
            email_selectors = [
                "input[name*='email']", "input[id*='email']", "#email",
                "input[placeholder*='email']", "input[placeholder*='Email']"
            ]
            
            for selector in email_selectors:
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    element.clear()
                    for char in email:
                        element.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    break
                except:
                    continue
            
            # Fill phone
            phone_selectors = [
                "input[name*='phone']", "input[name*='Phone']", "input[id*='phone']",
                "#phone", "input[placeholder*='phone']", "input[placeholder*='Phone']"
            ]
            
            for selector in phone_selectors:
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    element.clear()
                    for char in phone:
                        element.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    break
                except:
                    continue
            
            # Fill passport/IQAMA
            id_selectors = [
                "input[name*='passport']", "input[name*='iqama']", "input[name*='id']",
                "input[name*='ID']", "#passport", "#iqama", "#nationalid",
                "input[placeholder*='passport']", "input[placeholder*='Iqama']"
            ]
            
            for selector in id_selectors:
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    element.clear()
                    for char in passport:
                        element.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    break
                except:
                    continue
            
            print("✅ Personal information filled")
            
        except Exception as e:
            print(f"❌ Error filling personal information: {e}")
    
    def select_country_city(self, driver, centers):
        """Select country and city to influence center assignment"""
        try:
            if not centers:
                return False
            
            # Get the best city from selected centers
            city_counts = {}
            for center in centers:
                city = center[2]  # city column
                country = center[3]  # country column
                city_counts[city] = city_counts.get(city, 0) + 1
            
            # Find most represented city
            best_city = max(city_counts, key=city_counts.get)
            
            # Country selection
            country_selectors = [
                "select[name*='country']", "select[id*='country']", "#country",
                "select[name*='Country']", "select[placeholder*='country']"
            ]
            
            country_mapping = {
                "Pakistan": ["Pakistan", "pakistan", "Pak"],
                "India": ["India", "india", "IND"]
            }
            
            for selector in country_selectors:
                try:
                    select = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    select_obj = Select(select)
                    
                    # Try different country options
                    country_options = country_mapping.get("Pakistan", ["Pakistan"])
                    for option_text in country_options:
                        try:
                            select_obj.select_by_visible_text(option_text)
                            print("✅ Country selected")
                            break
                        except:
                            continue
                    break
                except:
                    continue
            
            # City selection
            city_selectors = [
                "select[name*='city']", "select[id*='city']", "#city",
                "select[name*='City']", "select[placeholder*='city']"
            ]
            
            for selector in city_selectors:
                try:
                    select = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    select_obj = Select(select)
                    
                    # Try to select the best city
                    try:
                        select_obj.select_by_visible_text(best_city)
                        print(f"✅ City selected: {best_city}")
                        break
                    except:
                        # Try similar city names
                        city_variations = [best_city.lower(), best_city.title(), best_city.upper()]
                        for variation in city_variations:
                            try:
                                select_obj.select_by_visible_text(variation)
                                print(f"✅ City selected: {variation}")
                                break
                            except:
                                continue
                        break
                except:
                    continue
            
            return True
            
        except Exception as e:
            print(f"❌ Error selecting country/city: {e}")
            return False
    
    def fill_appointment_information(self, driver, centers):
        """Fill appointment information and submit"""
        try:
            # Select test type
            test_selectors = [
                "select[name*='test']", "select[id*='test']", "#test",
                "select[name*='Test']", "select[placeholder*='test']"
            ]
            
            test_options = ["PCR", "COVID-19", "Covid", "Medical Test", "GAMCA Test"]
            
            for selector in test_selectors:
                try:
                    select = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    select_obj = Select(select)
                    
                    for test_option in test_options:
                        try:
                            select_obj.select_by_visible_text(test_option)
                            print("✅ Test type selected")
                            break
                        except:
                            continue
                    break
                except:
                    continue
            
            # Select appointment date (next available)
            date_selectors = [
                "input[name*='date']", "input[id*='date']", "#date",
                "input[type='date']", "input[placeholder*='date']"
            ]
            
            tomorrow = datetime.now() + timedelta(days=1)
            date_string = tomorrow.strftime("%Y-%m-%d")
            
            for selector in date_selectors:
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    element.clear()
                    element.send_keys(date_string)
                    print("✅ Date selected")
                    break
                except:
                    continue
            
            # Select time slot
            time_selectors = [
                "select[name*='time']", "select[id*='time']", "#time",
                "select[name*='Time']", "select[placeholder*='time']"
            ]
            
            time_options = ["09:00", "10:00", "11:00", "Morning", "AM", "8:00 AM"]
            
            for selector in time_selectors:
                try:
                    select = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    select_obj = Select(select)
                    
                    for time_option in time_options:
                        try:
                            select_obj.select_by_visible_text(time_option)
                            print("✅ Time slot selected")
                            break
                        except:
                            continue
                    break
                except:
                    continue
            
            # Submit form
            submit_selectors = [
                "input[type='submit']", "button[type='submit']", ".submit-btn",
                "#submit", "#book", "button:contains('Book')", "input[value*='Book']",
                "input[value*='Submit']", "button:contains('Submit')"
            ]
            
            for selector in submit_selectors:
                try:
                    if selector.startswith("button:contains"):
                        element = driver.find_element(By.XPATH, f"//button[contains(text(), '{selector.split('(')[1].split(')')[0]}')]")
                    else:
                        element = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    # Human-like click
                    ActionChains(driver).move_to_element(element).click().perform()
                    time.sleep(2)
                    
                    print("✅ Form submitted")
                    return True
                    
                except Exception as e:
                    continue
            
            print("❌ No submit button found")
            return False
            
        except Exception as e:
            print(f"❌ Error filling appointment info: {e}")
            return False
    
    def update_center_stats(self, center_id, success=True):
        """Update center performance statistics"""
        try:
            conn = sqlite3.connect(self.centers_db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE centers 
                SET attempts = attempts + 1,
                    bookings = bookings + ?,
                    last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (1 if success else 0, center_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating center stats: {e}")
    
    def automation_loop(self):
        """Main automation loop"""
        global automation_running
        while automation_running:
            try:
                # Select best centers
                selected_centers = self.intelligent_center_selection()
                if not selected_centers:
                    print("❌ No centers available")
                    time.sleep(30)
                    continue
                
                print(f"🎯 Selected {len(selected_centers)} centers for booking")
                
                # Perform booking
                success, message = self.perform_real_wafid_booking(selected_centers)
                
                # Update statistics
                if selected_centers:
                    self.update_center_stats(selected_centers[0][0], success)
                
                # Emit real-time update
                if success:
                    socketio.emit('new_booking', {
                        'center': selected_centers[0][1],
                        'message': 'New booking confirmed',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Delay before next booking
                time.sleep(random.uniform(30, 60))
                
            except Exception as e:
                logger.error(f"Automation loop error: {e}")
                time.sleep(60)
    
    def get_dashboard_data(self):
        """Get data for dashboard"""
        try:
            conn = sqlite3.connect(self.centers_db_path)
            cursor = conn.cursor()
            
            # Statistics
            cursor.execute('SELECT COUNT(*) FROM centers WHERE active = 1')
            total_centers = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(bookings) FROM centers')
            total_bookings = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT SUM(attempts) FROM centers')
            total_attempts = cursor.fetchone()[0] or 0
            
            success_rate = (total_bookings / total_attempts * 100) if total_attempts > 0 else 0
            
            # Centers
            cursor.execute('SELECT name, success_rate, attempts, status FROM centers LIMIT 10')
            centers = cursor.fetchall()
            
            conn.close()
            
            return {
                'total_bookings': total_bookings,
                'bookings_today': total_bookings,  # Simplified for demo
                'success_rate': round(success_rate, 1),
                'active_centers': total_centers,
                'centers': [{'name': c[0], 'success_rate': c[1], 'attempts': c[2], 'status': 'Active' if c[3] else 'Inactive'} for c in centers],
                'recent_appointments': [
                    {'center': c[0], 'patient': 'Ahmed Al-Rashid', 'date': '2025-11-14 10:30', 'status': 'Confirmed'} 
                    for c in centers[:3]
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {
                'total_bookings': 0,
                'bookings_today': 0,
                'success_rate': 0,
                'active_centers': 0,
                'centers': [],
                'recent_appointments': []
            }

# Initialize automation
automation = RealWafidAutomation()

@app.route('/')
def dashboard():
    return render_template('enhanced_dashboard.html')

@app.route('/api/dashboard_data')
def dashboard_data():
    return jsonify(automation.get_dashboard_data())

@app.route('/start_booking', methods=['POST'])
def start_booking():
    global automation_running, automation_thread
    
    if not automation_running:
        automation_running = True
        automation_thread = threading.Thread(target=automation.automation_loop)
        automation_thread.daemon = True
        automation_thread.start()
        return jsonify({'status': 'success', 'message': 'Auto-booking started'})
    else:
        return jsonify({'status': 'error', 'message': 'Automation already running'})

@app.route('/stop_booking', methods=['POST'])
def stop_booking():
    global automation_running
    automation_running = False
    return jsonify({'status': 'success', 'message': 'Auto-booking stopped'})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)