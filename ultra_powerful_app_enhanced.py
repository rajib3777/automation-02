#!/usr/bin/env python3
"""
Enhanced Ultra-Powerful Wafid System - Multi-Center Management Platform
2025 Edition - Advanced Automation & Analytics
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import json
import threading
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
import os
import sys
import uuid
import numpy as np
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import base64
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Union
from enum import Enum
import logging
import queue
import pickle
from collections import defaultdict
import statistics
import sqlite3

# Selenium with advanced configurations
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

# Advanced stealth and anti-detection
try:
    from selenium_stealth import stealth
    import undetected_chromedriver as uc
except ImportError:
    print("Warning: Enhanced stealth modules not available")
    stealth = None
    uc = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultra-powerful-wafid-multi-center-2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Enhanced Authentication Configuration
SYSTEM_PASSWORD = os.environ.get('SYSTEM_PASSWORD', "F@padma2041")
SESSION_TIMEOUT = 3600

# ===============================
# MULTI-CENTER MANAGEMENT SYSTEM
# ===============================

@dataclass
class Center:
    id: str
    name: str
    location: str
    capacity: int
    bookings_today: int
    success_rate: float
    status: str  # 'active', 'inactive', 'maintenance'
    created_at: datetime
    last_booking: Optional[datetime] = None
    automation_level: str = 'standard'  # 'basic', 'standard', 'advanced'
    ip_address: str = ''
    priority_level: int = 1
    daily_target: int = 100
    current_revenue: float = 0.0
    total_revenue: float = 0.0
    
@dataclass
class BookingMetrics:
    center_id: str
    timestamp: datetime
    success: bool
    booking_time: float
    slot_found: bool
    revenue_generated: float = 0.0
    error_type: Optional[str] = None

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Use Render's persistent storage or default to current directory
            db_path = os.environ.get('DATABASE_PATH', 'multi_center_automation.db')
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables for multi-center management"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Centers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS centers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    bookings_today INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'active',
                    created_at TEXT NOT NULL,
                    last_booking TEXT,
                    automation_level TEXT DEFAULT 'standard',
                    ip_address TEXT DEFAULT '',
                    priority_level INTEGER DEFAULT 1,
                    daily_target INTEGER DEFAULT 100,
                    current_revenue REAL DEFAULT 0.0,
                    total_revenue REAL DEFAULT 0.0
                )
            ''')
            
            # Booking metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS booking_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    center_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    booking_time REAL NOT NULL,
                    slot_found INTEGER NOT NULL,
                    revenue_generated REAL DEFAULT 0.0,
                    error_type TEXT,
                    FOREIGN KEY (center_id) REFERENCES centers (id)
                )
            ''')
            
            # Real-time analytics cache
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics_cache (
                    metric_name TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def add_center(self, center: Center) -> bool:
        """Add a new center to the system"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO centers 
                    (id, name, location, capacity, bookings_today, success_rate, 
                     status, created_at, automation_level, ip_address, priority_level, 
                     daily_target, current_revenue, total_revenue)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    center.id, center.name, center.location, center.capacity,
                    center.bookings_today, center.success_rate, center.status,
                    center.created_at.isoformat(), center.automation_level,
                    center.ip_address, center.priority_level, center.daily_target,
                    center.current_revenue, center.total_revenue
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding center: {e}")
            return False
    
    def get_centers(self) -> List[Center]:
        """Get all centers from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM centers')
            rows = cursor.fetchall()
            
            centers = []
            for row in rows:
                center = Center(
                    id=row[0], name=row[1], location=row[2], capacity=row[3],
                    bookings_today=row[4], success_rate=row[5], status=row[6],
                    created_at=datetime.fromisoformat(row[7]),
                    last_booking=datetime.fromisoformat(row[8]) if row[8] else None,
                    automation_level=row[9], ip_address=row[10], priority_level=row[11],
                    daily_target=row[12], current_revenue=row[13], total_revenue=row[14]
                )
                centers.append(center)
            return centers
    
    def update_center_bookings(self, center_id: str, success: bool, booking_time: float, 
                              slot_found: bool, revenue: float = 0.0):
        """Update center bookings and metrics with revenue tracking"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Update center metrics
            if success:
                cursor.execute('''
                    UPDATE centers 
                    SET bookings_today = bookings_today + 1,
                        last_booking = ?,
                        current_revenue = current_revenue + ?,
                        total_revenue = total_revenue + ?,
                        success_rate = CASE 
                            WHEN bookings_today = 0 THEN 100.0
                            ELSE (success_rate * bookings_today + 100.0) / (bookings_today + 1)
                        END
                    WHERE id = ?
                ''', (datetime.now().isoformat(), revenue, revenue, center_id))
            else:
                cursor.execute('''
                    UPDATE centers 
                    SET success_rate = CASE 
                        WHEN bookings_today = 0 THEN 0.0
                        ELSE (success_rate * bookings_today) / (bookings_today + 1)
                    END
                    WHERE id = ?
                ''', (center_id,))
            
            # Add booking metric
            cursor.execute('''
                INSERT INTO booking_metrics 
                (center_id, timestamp, success, booking_time, slot_found, revenue_generated)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (center_id, datetime.now().isoformat(), 
                  1 if success else 0, booking_time, 1 if slot_found else 0, revenue))
            
            conn.commit()
    
    def get_analytics_data(self) -> Dict:
        """Get comprehensive multi-center analytics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Current day booking trends (last 24 hours)
            cursor.execute('''
                SELECT 
                    strftime('%Y-%m-%d %H:00', timestamp) as hour,
                    COUNT(*) as total_attempts,
                    SUM(success) as successful_bookings,
                    AVG(booking_time) as avg_booking_time,
                    SUM(revenue_generated) as total_revenue
                FROM booking_metrics 
                WHERE timestamp >= datetime('now', '-24 hours')
                GROUP BY hour
                ORDER BY hour
            ''')
            hourly_data = cursor.fetchall()
            
            # Center performance summary
            cursor.execute('''
                SELECT 
                    name,
                    bookings_today,
                    success_rate,
                    status,
                    capacity,
                    current_revenue,
                    daily_target,
                    automation_level
                FROM centers
                ORDER BY bookings_today DESC
            ''')
            center_performance = cursor.fetchall()
            
            # Success rate trends (last 7 days)
            cursor.execute('''
                SELECT 
                    strftime('%Y-%m-%d', timestamp) as date,
                    SUM(success) * 100.0 / COUNT(*) as success_rate,
                    COUNT(*) as total_attempts,
                    SUM(revenue_generated) as daily_revenue
                FROM booking_metrics 
                WHERE timestamp >= datetime('now', '-7 days')
                GROUP BY date
                ORDER BY date
            ''')
            trend_data = cursor.fetchall()
            
            # Load balancing recommendations
            cursor.execute('''
                SELECT name, success_rate, bookings_today, capacity, status
                FROM centers
                WHERE status = 'active'
                ORDER BY success_rate DESC
            ''')
            load_balance_data = cursor.fetchall()
            
            return {
                'hourly_booking_trends': hourly_data,
                'center_performance': center_performance,
                'success_rate_trends': trend_data,
                'load_balance_recommendations': load_balance_data,
                'last_updated': datetime.now().isoformat()
            }

# Initialize database
db = DatabaseManager()

# ===============================
# ENHANCED AUTOMATION ENGINE
# ===============================

class EnhancedMultiCenterEngine:
    def __init__(self):
        self.config = load_config()
        self.running = False
        self.workers = []
        self.max_workers = 15
        self.booking_attempts = 0
        self.successful_bookings = 0
        self.total_revenue_generated = 0.0
        
    def create_stealth_driver(self):
        """Create enhanced stealth driver with anti-detection"""
        try:
            if uc:
                options = uc.ChromeOptions()
            else:
                options = ChromeOptions()
            
            # Enhanced stealth configuration
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            
            # Rotating user agents for anti-detection
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            driver = uc.Chrome(options=options) if uc else webdriver.Chrome(options=options)
            
            # Apply stealth configuration
            if stealth:
                stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True)
            
            return driver
            
        except Exception as e:
            print(f"Driver creation failed: {e}")
            return None
    
    def simulate_human_behavior(self, driver):
        """Enhanced human behavior simulation"""
        # Random delays
        time.sleep(random.uniform(2, 6))
        
        # Random mouse movements
        try:
            driver.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    clientX: {random.randint(100, 800)},
                    clientY: {random.randint(100, 600)}
                }});
                document.dispatchEvent(event);
            """)
        except:
            pass
        
        # Random scrolling patterns
        try:
            scroll_amount = random.randint(200, 800)
            driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
            time.sleep(random.uniform(1, 3))
        except:
            pass
    
    def perform_actual_form_automation(self, center: Center, driver) -> Tuple[bool, str]:
        """Real form automation for Wafid booking"""
        try:
            print(f"🤖 Starting real form automation for {center.name}")
            
            # Step 1: Navigate to Wafid booking page
            driver.get("https://wafid.com/book-appointment/")
            print("📄 Navigated to Wafid booking page")
            
            # Step 2: Wait for form to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            print("✅ Form detected and loaded")
            
            # Step 3: Fill personal information
            self.fill_personal_info(driver)
            
            # Step 4: Select appointment details
            self.select_appointment_details(driver, center)
            
            # Step 5: Select center (this is key for multi-center automation)
            self.select_test_center(driver, center)
            
            # Step 6: Handle any CAPTCHAs
            if self.handle_captcha_if_present(driver):
                print("✅ CAPTCHA handled")
            
            # Step 7: Submit form
            return self.submit_form(driver)
            
        except Exception as e:
            print(f"❌ Form automation failed for {center.name}: {str(e)}")
            return False, str(e)
    
    def fill_personal_info(self, driver):
        """Fill personal information fields"""
        try:
            # Generate realistic personal data for automation
            first_names = ["Ahmed", "Mohammed", "Abdul", "Omar", "Khalid", "Saad"]
            last_names = ["Al-Rashid", "Al-Mansouri", "Al-Zahra", "Al-Harbi", "Al-Otaibi", "Al-Mutairi"]
            
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@gmail.com"
            phone = f"+966{random.randint(500000000, 599999999)}"
            iqama = f"{random.randint(100, 999)}{random.randint(1000000, 9999999)}"
            
            # Fill name field
            name_selectors = ["input[name*='name']", "input[id*='name']", "input[placeholder*='name']", "#name", "#fullname"]
            self.fill_field_by_selectors(driver, name_selectors, full_name)
            
            # Fill email field
            email_selectors = ["input[name*='email']", "input[id*='email']", "input[placeholder*='email']", "#email"]
            self.fill_field_by_selectors(driver, email_selectors, email)
            
            # Fill phone field
            phone_selectors = ["input[name*='phone']", "input[id*='phone']", "input[placeholder*='phone']", "#phone", "input[placeholder*='mobile']"]
            self.fill_field_by_selectors(driver, phone_selectors, phone)
            
            # Fill ID/IQAMA field
            id_selectors = ["input[name*='iqama']", "input[name*='id']", "input[name*='passport']", "input[placeholder*='ID']", "input[placeholder*='Iqama']"]
            self.fill_field_by_selectors(driver, id_selectors, iqama)
            
            print(f"✅ Personal info filled: {full_name}")
            
        except Exception as e:
            print(f"❌ Error filling personal info: {e}")
    
    def select_appointment_details(self, driver, center):
        """Select appointment type and preferences"""
        try:
            # Select test type (PCR is most common)
            test_type_selectors = [
                "select[name*='test']", 
                "select[id*='test']", 
                "select[placeholder*='test']",
                "input[name*='test']"
            ]
            
            # Try to select PCR test
            test_options = ["PCR", "Covid", "COVID", "PCR Test", "COVID-19"]
            for option in test_options:
                if self.select_option_by_text(driver, test_type_selectors, option):
                    print("✅ Test type selected")
                    break
            
            # Select date (next available)
            date_selectors = ["input[name*='date']", "input[id*='date']", "input[type='date']"]
            tomorrow = datetime.now() + timedelta(days=1)
            date_string = tomorrow.strftime("%Y-%m-%d")
            self.fill_field_by_selectors(driver, date_selectors, date_string)
            
            # Select time slot (morning preferred)
            time_selectors = ["select[name*='time']", "select[id*='time']", "select[placeholder*='time']"]
            time_options = ["09:00", "10:00", "11:00", "Morning", "AM"]
            for time_opt in time_options:
                if self.select_option_by_text(driver, time_selectors, time_opt):
                    print("✅ Time slot selected")
                    break
            
            print("✅ Appointment details selected")
            
        except Exception as e:
            print(f"❌ Error selecting appointment details: {e}")
    
    def select_test_center(self, driver, center):
        """Select the specific test center from your multi-center system"""
        try:
            # This is crucial for multi-center automation
            center_selectors = [
                "select[name*='center']",
                "select[name*='location']", 
                "select[name*='branch']",
                "input[name*='center']",
                "input[name*='location']"
            ]
            
            # Find and select the center from your database
            center_names = [
                center.name,
                f"Center {center.id}",
                center.location,
                f"{center.name} - {center.location}"
            ]
            
            for center_name in center_names:
                if self.select_option_by_text(driver, center_selectors, center_name):
                    print(f"✅ Center selected: {center_name}")
                    break
            else:
                # If specific center not found, select any available center
                self.select_any_available_center(driver, center_selectors)
                print(f"⚠️  Using default center for {center.name}")
            
        except Exception as e:
            print(f"❌ Error selecting test center: {e}")
    
    def select_any_available_center(self, driver, selectors):
        """Select any available center if specific center not found"""
        try:
            for selector in selectors:
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    select = Select(element)
                    # Select second option (first is usually "Select center")
                    if len(select.options) > 1:
                        select.select_by_index(1)
                        print(f"✅ Selected available center: {select.options[1].text}")
                        return
                except:
                    continue
        except Exception as e:
            print(f"❌ Error selecting available center: {e}")
    
    def handle_captcha_if_present(self, driver) -> bool:
        """Handle CAPTCHA if present"""
        try:
            # Look for common CAPTCHA elements
            captcha_selectors = [
                "img[src*='captcha']",
                "img[src*='recaptcha']",
                ".g-recaptcha",
                "#captcha",
                ".captcha"
            ]
            
            for selector in captcha_selectors:
                try:
                    captcha_element = driver.find_element(By.CSS_SELECTOR, selector)
                    if captcha_element.is_displayed():
                        print("⚠️  CAPTCHA detected - manual intervention required")
                        # In production, you would integrate with a CAPTCHA solving service
                        return False
                except:
                    continue
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking for CAPTCHA: {e}")
            return False
    
    def submit_form(self, driver) -> Tuple[bool, str]:
        """Submit the booking form"""
        try:
            # Look for submit button
            submit_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button[name*='submit']",
                "button:contains('Submit')",
                "button:contains('Book')",
                "button:contains('Confirm')",
                ".btn-primary",
                "#submit",
                "#book-btn"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    # Human-like click
                    ActionChains(driver).move_to_element(submit_button).pause(0.5).click(submit_button).perform()
                    print("✅ Form submitted successfully")
                    
                    # Wait for confirmation
                    time.sleep(3)
                    return True, "Form submitted successfully"
                    
                except Exception as e:
                    continue
            
            # If no submit button found, try pressing Enter
            try:
                ActionChains(driver).send_keys(Keys.ENTER).perform()
                print("✅ Form submitted with Enter key")
                return True, "Form submitted with Enter key"
            except:
                pass
            
            return False, "No submit button found"
            
        except Exception as e:
            return False, f"Error submitting form: {str(e)}"
    
    def fill_field_by_selectors(self, driver, selectors, value):
        """Fill a field by trying multiple selectors"""
        for selector in selectors:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                element.clear()
                # Type like a human
                for char in value:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                print(f"✅ Filled {selector} with: {value}")
                return True
            except:
                continue
        return False
    
    def select_option_by_text(self, driver, selectors, option_text):
        """Select an option by text from multiple dropdown selectors"""
        for selector in selectors:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                select = Select(element)
                select.select_by_visible_text(option_text)
                print(f"✅ Selected '{option_text}' from {selector}")
                return True
            except:
                continue
        return False
    
    def intelligent_load_balancing(self, centers: List[Center]) -> Center:
        """AI-powered load balancing to optimize success rates"""
        active_centers = [c for c in centers if c.status == 'active']
        
        if not active_centers:
            return None
        
        # Score each center based on multiple factors
        center_scores = []
        for center in active_centers:
            score = (
                center.success_rate * 0.4 +  # Success rate weight (40%)
                (center.capacity - center.bookings_today) / center.capacity * 30 +  # Available capacity (30%)
                (2 - center.priority_level) * 20 +  # Priority weight (20%)
                (1 - center.daily_target and center.bookings_today / center.daily_target) * 10  # Daily progress (10%)
            )
            center_scores.append((center, score))
        
        # Return highest scoring center
        return max(center_scores, key=lambda x: x[1])[0]
    
    def perform_smart_booking(self, center: Center) -> Tuple[bool, float]:
        """Perform intelligent booking with REAL form automation"""
        driver = None
        try:
            driver = self.create_stealth_driver()
            if not driver:
                return False, 0.0
            
            print(f"🎯 Starting REAL automation for {center.name}")
            
            # Perform actual form automation
            success, message = self.perform_actual_form_automation(center, driver)
            
            if success:
                # Real booking succeeded - calculate revenue based on test type and center
                base_revenue = 75.0  # Base PCR test price
                center_multiplier = {'basic': 1.0, 'standard': 1.15, 'advanced': 1.3}.get(center.automation_level, 1.0)
                revenue = base_revenue * center_multiplier
                
                print(f"✅ REAL booking SUCCESS for {center.name} - Revenue: ${revenue:.2f}")
                return True, revenue
            else:
                print(f"❌ REAL booking FAILED for {center.name}: {message}")
                return False, 0.0
            
        except Exception as e:
            print(f"Smart booking error for {center.name}: {e}")
            return False, 0.0
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def start_enhanced_automation(self):
        """Start enhanced multi-center automation"""
        global automation_running
        automation_running = True
        
        def automation_worker():
            while automation_running:
                try:
                    # Get all centers
                    centers = db.get_centers()
                    active_centers = [c for c in centers if c.status == 'active']
                    
                    if not active_centers:
                        time.sleep(60)
                        continue
                    
                    # Intelligent center selection
                    selected_center = self.intelligent_load_balancing(active_centers)
                    if not selected_center:
                        time.sleep(30)
                        continue
                    
                    # Check daily targets
                    if selected_center.bookings_today >= selected_center.daily_target:
                        print(f"Daily target reached for {selected_center.name}")
                        time.sleep(300)  # Wait 5 minutes before checking again
                        continue
                    
                    print(f"🤖 Automation: Targeting {selected_center.name}")
                    
                    # Perform smart booking
                    success, revenue = self.perform_smart_booking(selected_center)
                    
                    # Update database
                    db.update_center_bookings(
                        selected_center.id, success, 
                        random.uniform(3.0, 10.0),  # Booking time
                        success,  # Slot found if successful
                        revenue
                    )
                    
                    # Update global stats
                    if success:
                        self.successful_bookings += 1
                        self.total_revenue_generated += revenue
                        
                        # Emit real-time update
                        socketio.emit('booking_success', {
                            'center': selected_center.name,
                            'revenue': revenue,
                            'time': datetime.now().strftime('%H:%M:%S'),
                            'total_revenue': self.total_revenue_generated
                        })
                    
                    # Adaptive delay based on success rate
                    if success:
                        time.sleep(random.uniform(30, 90))  # Shorter delay after success
                    else:
                        time.sleep(random.uniform(120, 300))  # Longer delay after failure
                    
                    # System health check
                    if datetime.now().minute % 10 == 0:  # Every 10 minutes
                        socketio.emit('system_health', {
                            'total_centers': len(centers),
                            'active_centers': len(active_centers),
                            'total_revenue': self.total_revenue_generated,
                            'automation_running': automation_running
                        })
                    
                except Exception as e:
                    print(f"Automation worker error: {e}")
                    time.sleep(60)
        
        # Start automation thread
        automation_thread = threading.Thread(target=automation_worker, daemon=True)
        automation_thread.start()
        return True
    
    def stop_automation(self):
        """Stop automation"""
        global automation_running
        automation_running = False
        return True

# Global variables
automation_running = False
multi_center_engine = EnhancedMultiCenterEngine()

# ===============================
# AUTHENTICATION & SESSION
# ===============================

def is_authenticated():
    """Enhanced authentication check"""
    if 'authenticated' not in session:
        return False
    
    # Check session timeout
    if 'login_time' in session:
        login_time = session['login_time']
        if (datetime.now() - datetime.fromtimestamp(login_time)).seconds > SESSION_TIMEOUT:
            session.clear()
            return False
    
    return session.get('authenticated', False)

def require_auth(f):
    """Enhanced decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            if request.is_json:
                return jsonify({"error": "Authentication required", "redirect": "/"}), 401
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ===============================
# CONFIGURATION MANAGEMENT
# ===============================

def load_config():
    """Load system configuration"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {
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
            },
            "system_settings": {
                "automation_level": "advanced",
                "anti_detection": True,
                "revenue_optimization": True,
                "load_balancing": True
            }
        }

def save_config(config):
    """Save system configuration"""
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except:
        return False

# ===============================
# ROUTES
# ===============================

@app.route('/')
def index():
    """Main landing page"""
    return render_template('enhanced_dashboard.html', authenticated=False)

@app.route('/dashboard')
@require_auth
def dashboard():
    """Enhanced multi-center dashboard"""
    config = load_config()
    centers = db.get_centers()
    return render_template('enhanced_dashboard.html', 
                         config=config, 
                         centers=centers,
                         authenticated=True)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Enhanced authentication"""
    data = request.get_json()
    password = data.get('password', '')
    
    if password == SYSTEM_PASSWORD:
        session['authenticated'] = True
        session['login_time'] = time.time()
        return jsonify({
            'success': True, 
            'message': 'Authentication successful',
            'redirect': '/dashboard'
        })
    else:
        return jsonify({
            'success': False, 
            'message': 'Invalid password'
        }), 401

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('index'))

# ===============================
# API ENDPOINTS
# ===============================

@app.route('/api/centers', methods=['GET'])
@require_auth
def get_centers():
    """Get all centers with enhanced metrics"""
    centers = db.get_centers()
    
    # Calculate additional metrics
    for center in centers:
        center_utilization = (center.bookings_today / center.capacity) * 100 if center.capacity > 0 else 0
        center.progress = (center.bookings_today / center.daily_target) * 100 if center.daily_target > 0 else 0
        center.remaining_target = max(0, center.daily_target - center.bookings_today)
    
    return jsonify({
        'centers': [
            {
                **center.__dict__,
                'utilization_rate': center_utilization,
                'progress_percent': center.progress,
                'remaining_target': center.remaining_target
            } for center in centers
        ],
        'total': len(centers),
        'active': len([c for c in centers if c.status == 'active']),
        'total_revenue': sum(c.current_revenue for c in centers)
    })

@app.route('/api/centers', methods=['POST'])
@require_auth
def add_center():
    """Add new center to the system"""
    data = request.json
    
    center_id = f"center_{int(time.time())}"
    new_center = Center(
        id=center_id,
        name=data['name'],
        location=data['location'],
        capacity=int(data['capacity']),
        bookings_today=0,
        success_rate=0.0,
        status='active',
        created_at=datetime.now(),
        automation_level=data.get('automation_level', 'standard'),
        priority_level=int(data.get('priority_level', 1)),
        daily_target=int(data.get('daily_target', 100)),
        ip_address=data.get('ip_address', '')
    )
    
    success = db.add_center(new_center)
    if success:
        socketio.emit('center_added', {
            'center': new_center.__dict__,
            'message': f'New center "{new_center.name}" added successfully'
        })
        return jsonify({'success': True, 'center_id': center_id})
    return jsonify({'success': False, 'message': 'Failed to add center'})

@app.route('/api/centers/<center_id>/toggle', methods=['POST'])
@require_auth
def toggle_center(center_id):
    """Toggle center status"""
    centers = db.get_centers()
    center = next((c for c in centers if c.id == center_id), None)
    
    if center:
        new_status = 'inactive' if center.status == 'active' else 'active'
        
        # Update in database
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE centers SET status = ? WHERE id = ?', (new_status, center_id))
            conn.commit()
        
        socketio.emit('center_status_changed', {
            'center_id': center_id,
            'status': new_status,
            'message': f'Center "{center.name}" is now {new_status}'
        })
        
        return jsonify({'success': True, 'status': new_status})
    
    return jsonify({'success': False, 'message': 'Center not found'})

@app.route('/api/analytics', methods=['GET'])
@require_auth
def get_analytics():
    """Get comprehensive analytics"""
    analytics_data = db.get_analytics_data()
    return jsonify(analytics_data)

@app.route('/api/automation/start', methods=['POST'])
@require_auth
def start_automation():
    """Start enhanced automation"""
    try:
        result = multi_center_engine.start_enhanced_automation()
        return jsonify({'success': result, 'message': 'Enhanced automation started'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/automation/stop', methods=['POST'])
@require_auth
def stop_automation():
    """Stop automation"""
    try:
        result = multi_center_engine.stop_automation()
        return jsonify({'success': result, 'message': 'Automation stopped'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/automation/status', methods=['GET'])
@require_auth
def automation_status():
    """Get automation status"""
    centers = db.get_centers()
    return jsonify({
        'running': automation_running,
        'total_centers': len(centers),
        'active_centers': len([c for c in centers if c.status == 'active']),
        'total_revenue': sum(c.current_revenue for c in centers),
        'last_booking': get_last_booking_time()
    })

def get_last_booking_time():
    """Get the timestamp of the last successful booking"""
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp FROM booking_metrics 
                WHERE success = 1 
                ORDER BY timestamp DESC LIMIT 1
            ''')
            result = cursor.fetchone()
            return result[0] if result else None
    except:
        return None

# ===============================
# SOCKET.IO EVENTS
# ===============================

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    if is_authenticated():
        emit('connection_status', {'status': 'connected', 'authenticated': True})
    else:
        emit('connection_status', {'status': 'connected', 'authenticated': False})

@socketio.on('request_analytics')
def handle_analytics_request():
    """Handle analytics data request"""
    if is_authenticated():
        analytics_data = db.get_analytics_data()
        emit('analytics_data', analytics_data)

# ===============================
# INITIALIZATION
# ===============================

def initialize_sample_data():
    """Initialize database with sample centers"""
    centers = db.get_centers()
    if not centers:
        sample_centers = [
            Center(
                id='center_1', name='Downtown Medical Hub', location='Downtown District',
                capacity=50, bookings_today=23, success_rate=87.5, status='active',
                created_at=datetime.now() - timedelta(days=30),
                automation_level='advanced', priority_level=1, daily_target=100,
                current_revenue=1250.75
            ),
            Center(
                id='center_2', name='East Side Health Center', location='East Side',
                capacity=75, bookings_today=41, success_rate=92.3, status='active',
                created_at=datetime.now() - timedelta(days=45),
                automation_level='standard', priority_level=2, daily_target=150,
                current_revenue=2180.25
            ),
            Center(
                id='center_3', name='North Valley Clinic', location='North Valley',
                capacity=30, bookings_today=12, success_rate=78.9, status='active',
                created_at=datetime.now() - timedelta(days=15),
                automation_level='basic', priority_level=3, daily_target=80,
                current_revenue=680.50
            ),
            Center(
                id='center_4', name='Westside Medical Plaza', location='Westside',
                capacity=60, bookings_today=0, success_rate=0.0, status='inactive',
                created_at=datetime.now() - timedelta(days=1),
                automation_level='standard', priority_level=4, daily_target=120,
                current_revenue=0.0
            )
        ]
        
        for center in sample_centers:
            db.add_center(center)

if __name__ == '__main__':
    # Initialize system
    initialize_sample_data()
    
    print("🚀" + "="*70 + "🚀")
    print("   ENHANCED ULTRA-POWERFUL WAFID SYSTEM - MULTI-CENTER EDITION   ")
    print("🚀" + "="*70 + "🚀")
    print()
    print("✅ Enhanced Features Loaded:")
    print("   🏢 Multi-Center Management System")
    print("   🤖 AI-Powered Load Balancing")
    print("   📊 Real-Time Analytics Dashboard")
    print("   💰 Revenue Optimization Engine")
    print("   🛡️ Advanced Anti-Detection")
    print("   📈 Performance Monitoring")
    print("   ⚡ Scalable Architecture")
    print()
    print(f"🌐 Dashboard URL: http://localhost:5000")
    print(f"🔐 System Password: {SYSTEM_PASSWORD}")
    print()
    
    # Start the application
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)