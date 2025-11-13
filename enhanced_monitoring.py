"""
Enhanced Monitoring System for Wafid Booking Bot
Provides comprehensive monitoring, retry logic, and backup strategies
"""

import time
import random
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import threading
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException,
    StaleElementReferenceException, ElementNotInteractableException
)

class FailureType(Enum):
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    CAPTCHA_DETECTED = "captcha_detected"
    FORM_ERROR = "form_error"
    WEBSITE_DOWN = "website_down"
    BROWSER_CRASH = "browser_crash"
    NO_SLOTS_AVAILABLE = "no_slots_available"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class AttemptResult:
    success: bool
    failure_type: Optional[FailureType]
    error_message: str
    timestamp: datetime
    response_time: float
    center_assigned: Optional[str] = None

@dataclass
class HealthStatus:
    website_accessible: bool
    response_time: float
    last_check: datetime
    error_count: int
    consecutive_failures: int

class EnhancedMonitor:
    def __init__(self, socketio_instance=None):
        self.socketio = socketio_instance
        self.attempt_history: List[AttemptResult] = []
        self.health_status = HealthStatus(
            website_accessible=True,
            response_time=0.0,
            last_check=datetime.now(),
            error_count=0,
            consecutive_failures=0
        )
        
        # Monitoring configuration
        self.config = {
            "max_retries": 5,
            "retry_delays": [2, 5, 10, 20, 30],  # Progressive delays in seconds
            "health_check_interval": 60,  # Check every minute
            "success_validation_timeout": 30,
            "captcha_detection_keywords": ["captcha", "robot", "verify", "security"],
            "network_timeout": 15,
            "max_consecutive_failures": 3
        }
        
        # Statistics
        self.stats = {
            "total_attempts": 0,
            "successful_attempts": 0,
            "retry_success_rate": 0.0,
            "average_response_time": 0.0,
            "failure_breakdown": {ft.value: 0 for ft in FailureType},
            "peak_performance_hours": {},
            "last_success_time": None
        }
        
        # Start background health monitoring
        self.start_health_monitoring()
    
    def emit_update(self, message: str, level: str = "info"):
        """Send real-time updates to dashboard"""
        if self.socketio:
            self.socketio.emit('monitoring_update', {
                "message": message,
                "level": level,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "stats": self.get_stats_summary()
            })
    
    def classify_error(self, error: Exception, page_source: str = "") -> FailureType:
        """Intelligently classify the type of error encountered"""
        error_str = str(error).lower()
        page_source_lower = page_source.lower()
        
        # Network-related errors
        if any(keyword in error_str for keyword in ["connection", "network", "unreachable", "timeout"]):
            return FailureType.NETWORK_ERROR
        
        # Timeout errors
        if "timeout" in error_str or isinstance(error, TimeoutException):
            return FailureType.TIMEOUT
        
        # CAPTCHA detection
        if any(keyword in page_source_lower for keyword in self.config["captcha_detection_keywords"]):
            return FailureType.CAPTCHA_DETECTED
        
        # Browser/driver issues
        if any(keyword in error_str for keyword in ["webdriver", "chrome", "browser", "session"]):
            return FailureType.BROWSER_CRASH
        
        # Form-related errors
        if any(keyword in error_str for keyword in ["element", "clickable", "interact"]):
            return FailureType.FORM_ERROR
        
        # No slots available (common Wafid response)
        if any(keyword in page_source_lower for keyword in ["no slots", "not available", "fully booked"]):
            return FailureType.NO_SLOTS_AVAILABLE
        
        return FailureType.UNKNOWN_ERROR
    
    def record_attempt(self, success: bool, error: Exception = None, 
                      response_time: float = 0.0, center: str = None, 
                      page_source: str = "") -> AttemptResult:
        """Record the result of a booking attempt"""
        failure_type = None
        error_message = ""
        
        if not success and error:
            failure_type = self.classify_error(error, page_source)
            error_message = str(error)
            self.stats["failure_breakdown"][failure_type.value] += 1
        
        result = AttemptResult(
            success=success,
            failure_type=failure_type,
            error_message=error_message,
            timestamp=datetime.now(),
            response_time=response_time,
            center_assigned=center
        )
        
        self.attempt_history.append(result)
        self.update_stats(result)
        
        # Keep only last 1000 attempts to prevent memory issues
        if len(self.attempt_history) > 1000:
            self.attempt_history = self.attempt_history[-1000:]
        
        return result
    
    def update_stats(self, result: AttemptResult):
        """Update monitoring statistics"""
        self.stats["total_attempts"] += 1
        
        if result.success:
            self.stats["successful_attempts"] += 1
            self.stats["last_success_time"] = result.timestamp
            self.health_status.consecutive_failures = 0
        else:
            self.health_status.consecutive_failures += 1
        
        # Update success rate
        self.stats["retry_success_rate"] = (
            self.stats["successful_attempts"] / self.stats["total_attempts"] * 100
        ) if self.stats["total_attempts"] > 0 else 0
        
        # Update average response time
        total_time = sum(attempt.response_time for attempt in self.attempt_history)
        self.stats["average_response_time"] = total_time / len(self.attempt_history)
        
        # Track peak performance hours
        hour = result.timestamp.hour
        if hour not in self.stats["peak_performance_hours"]:
            self.stats["peak_performance_hours"][hour] = {"attempts": 0, "successes": 0}
        
        self.stats["peak_performance_hours"][hour]["attempts"] += 1
        if result.success:
            self.stats["peak_performance_hours"][hour]["successes"] += 1
    
    def should_retry(self, attempt_count: int, last_failure: FailureType) -> Tuple[bool, int]:
        """Determine if we should retry and what delay to use"""
        # Don't retry if we've hit max attempts
        if attempt_count >= self.config["max_retries"]:
            return False, 0
        
        # Don't retry for certain failure types
        if last_failure in [FailureType.CAPTCHA_DETECTED]:
            self.emit_update("❌ CAPTCHA detected - Manual intervention required", "warning")
            return False, 0
        
        # Increase delay for consecutive failures
        base_delay = self.config["retry_delays"][min(attempt_count, len(self.config["retry_delays"]) - 1)]
        
        # Add randomization to prevent thundering herd
        delay = base_delay + random.uniform(0, base_delay * 0.3)
        
        # Increase delay if website health is poor
        if self.health_status.consecutive_failures > 2:
            delay *= 2
            
        return True, int(delay)
    
    def check_website_health(self) -> bool:
        """Check if Wafid website is accessible and responsive"""
        try:
            start_time = time.time()
            response = requests.get(
                "https://wafid.com/book-appointment/",
                timeout=self.config["network_timeout"],
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.health_status.website_accessible = True
                self.health_status.response_time = response_time
                self.health_status.error_count = 0
                return True
            else:
                self.health_status.website_accessible = False
                self.health_status.error_count += 1
                return False
                
        except Exception as e:
            self.health_status.website_accessible = False
            self.health_status.error_count += 1
            self.emit_update(f"⚠️ Website health check failed: {str(e)}", "warning")
            return False
        finally:
            self.health_status.last_check = datetime.now()
    
    def start_health_monitoring(self):
        """Start background health monitoring thread"""
        def health_monitor():
            while True:
                try:
                    is_healthy = self.check_website_health()
                    
                    if not is_healthy and self.health_status.error_count >= 3:
                        self.emit_update(
                            f"🚨 Website appears to be down (Response time: {self.health_status.response_time:.2f}s)",
                            "error"
                        )
                    elif is_healthy and self.health_status.response_time > 5:
                        self.emit_update(
                            f"⚠️ Website is slow (Response time: {self.health_status.response_time:.2f}s)",
                            "warning"
                        )
                    
                    time.sleep(self.config["health_check_interval"])
                    
                except Exception as e:
                    self.emit_update(f"Health monitor error: {str(e)}", "error")
                    time.sleep(30)  # Shorter retry on monitor errors
        
        health_thread = threading.Thread(target=health_monitor, daemon=True)
        health_thread.start()
    
    def validate_booking_success(self, driver, expected_center: str = None) -> Tuple[bool, str]:
        """Validate that booking was actually successful"""
        try:
            # Look for success indicators on the page
            success_indicators = [
                "booking confirmed",
                "appointment scheduled",
                "successfully booked",
                "confirmation number",
                "reference number"
            ]
            
            page_source = driver.page_source.lower()
            
            for indicator in success_indicators:
                if indicator in page_source:
                    # Try to extract confirmation details
                    confirmation_info = self.extract_confirmation_details(driver)
                    return True, confirmation_info
            
            return False, "No success confirmation found"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def extract_confirmation_details(self, driver) -> str:
        """Extract booking confirmation details"""
        try:
            # Common selectors for confirmation info
            selectors = [
                "confirmation-number",
                "booking-reference",
                "appointment-details",
                ".success-message",
                "#confirmation"
            ]
            
            for selector in selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    if element.text.strip():
                        return element.text.strip()
                except:
                    continue
            
            return "Booking confirmed (details not extracted)"
            
        except Exception:
            return "Booking confirmed"
    
    def get_stats_summary(self) -> Dict:
        """Get a summary of current statistics"""
        return {
            "total_attempts": self.stats["total_attempts"],
            "success_rate": f"{self.stats['retry_success_rate']:.1f}%",
            "avg_response_time": f"{self.stats['average_response_time']:.2f}s",
            "website_health": "Healthy" if self.health_status.website_accessible else "Issues",
            "consecutive_failures": self.health_status.consecutive_failures,
            "last_success": self.stats["last_success_time"].strftime("%H:%M:%S") if self.stats["last_success_time"] else "None"
        }
    
    def get_failure_analysis(self) -> Dict:
        """Get detailed failure analysis"""
        total_failures = sum(self.stats["failure_breakdown"].values())
        
        if total_failures == 0:
            return {"message": "No failures recorded yet"}
        
        analysis = {}
        for failure_type, count in self.stats["failure_breakdown"].items():
            if count > 0:
                percentage = (count / total_failures) * 100
                analysis[failure_type] = {
                    "count": count,
                    "percentage": f"{percentage:.1f}%"
                }
        
        return analysis
    
    def get_peak_hours_analysis(self) -> Dict:
        """Analyze peak performance hours"""
        peak_analysis = {}
        
        for hour, data in self.stats["peak_performance_hours"].items():
            if data["attempts"] > 0:
                success_rate = (data["successes"] / data["attempts"]) * 100
                peak_analysis[f"{hour:02d}:00"] = {
                    "attempts": data["attempts"],
                    "success_rate": f"{success_rate:.1f}%"
                }
        
        return peak_analysis