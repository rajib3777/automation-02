"""
Center Management System for Enhanced Wafid Booking Bot
Handles multiple preferred centers with priority-based targeting
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
import time
import random

class CenterStatus(Enum):
    AVAILABLE = "available"
    FULLY_BOOKED = "fully_booked"
    UNKNOWN = "unknown"
    ERROR = "error"

@dataclass
class PreferredCenter:
    name: str
    priority: int  # 1 = highest priority
    success_count: int = 0
    attempt_count: int = 0
    last_success_time: Optional[str] = None
    status: CenterStatus = CenterStatus.UNKNOWN
    average_response_time: float = 0.0
    best_booking_hours: List[int] = None
    
    @property
    def success_rate(self) -> float:
        if self.attempt_count == 0:
            return 0.0
        return (self.success_count / self.attempt_count) * 100
    
    def __post_init__(self):
        if self.best_booking_hours is None:
            self.best_booking_hours = []

class CenterManager:
    def __init__(self, socketio_instance=None):
        self.socketio = socketio_instance
        
        # User's 3 preferred centers in priority order
        self.preferred_centers = [
            PreferredCenter(
                name="Precision Diagnostics Ltd",
                priority=1
            ),
            PreferredCenter(
                name="Mediquest Diagnostics Ltd", 
                priority=2
            ),
            PreferredCenter(
                name="Allied Diagnostics Ltd",
                priority=3
            )
        ]
        
        # Center targeting configuration
        self.config = {
            "max_attempts_per_center": 3,
            "center_switch_delay": 5,  # seconds between center attempts
            "preferred_center_bonus_attempts": 2,  # extra attempts for priority 1
            "track_peak_hours": True,
            "smart_center_selection": True
        }
        
        # Statistics tracking
        self.session_stats = {
            "centers_attempted": [],
            "current_target_center": None,
            "successful_center": None,
            "total_center_switches": 0
        }
    
    def emit_update(self, message: str, level: str = "info"):
        """Send center-specific updates to dashboard"""
        if self.socketio:
            self.socketio.emit('center_update', {
                "message": message,
                "level": level,
                "timestamp": time.strftime("%H:%M:%S"),
                "current_target": self.session_stats.get("current_target_center"),
                "centers_status": self.get_centers_status_summary()
            })
    
    def get_next_target_center(self, exclude_centers: List[str] = None) -> Optional[PreferredCenter]:
        """Get the next center to target based on priority and performance"""
        exclude_centers = exclude_centers or []
        
        # Filter out excluded centers
        available_centers = [
            center for center in self.preferred_centers 
            if center.name not in exclude_centers
        ]
        
        if not available_centers:
            return None
        
        if self.config["smart_center_selection"]:
            # Smart selection based on success rate and priority
            return self._smart_center_selection(available_centers)
        else:
            # Simple priority-based selection
            return min(available_centers, key=lambda x: x.priority)
    
    def _smart_center_selection(self, available_centers: List[PreferredCenter]) -> PreferredCenter:
        """Intelligent center selection based on multiple factors"""
        current_hour = time.localtime().tm_hour
        
        # Score each center
        scored_centers = []
        for center in available_centers:
            score = 0
            
            # Priority bonus (higher priority = lower number = higher score)
            score += (4 - center.priority) * 30
            
            # Success rate bonus
            score += center.success_rate * 0.5
            
            # Peak hour bonus
            if current_hour in center.best_booking_hours:
                score += 20
            
            # Recent success bonus
            if center.last_success_time:
                score += 10
            
            # Avoid centers with recent failures
            if center.status == CenterStatus.FULLY_BOOKED:
                score -= 15
            
            scored_centers.append((center, score))
        
        # Sort by score (highest first) and return best center
        scored_centers.sort(key=lambda x: x[1], reverse=True)
        selected_center = scored_centers[0][0]
        
        self.emit_update(f"🎯 Smart selection: {selected_center.name} (Score: {scored_centers[0][1]:.1f})")
        return selected_center
    
    def record_center_attempt(self, center_name: str, success: bool, response_time: float = 0.0):
        """Record the result of a booking attempt at a specific center"""
        center = self.get_center_by_name(center_name)
        if not center:
            return
        
        center.attempt_count += 1
        
        if success:
            center.success_count += 1
            center.last_success_time = time.strftime("%H:%M:%S")
            center.status = CenterStatus.AVAILABLE
            self.session_stats["successful_center"] = center_name
            
            # Track peak hours
            if self.config["track_peak_hours"]:
                current_hour = time.localtime().tm_hour
                if current_hour not in center.best_booking_hours:
                    center.best_booking_hours.append(current_hour)
            
            self.emit_update(f"🎉 SUCCESS at {center_name}! (Success rate: {center.success_rate:.1f}%)", "success")
        else:
            center.status = CenterStatus.FULLY_BOOKED
            self.emit_update(f"❌ No slots at {center_name} (Attempt {center.attempt_count})", "warning")
        
        # Update average response time
        if response_time > 0:
            total_time = center.average_response_time * (center.attempt_count - 1) + response_time
            center.average_response_time = total_time / center.attempt_count
    
    def get_center_by_name(self, name: str) -> Optional[PreferredCenter]:
        """Get center object by name"""
        for center in self.preferred_centers:
            if center.name.lower() == name.lower():
                return center
        return None
    
    def should_switch_center(self, current_center_name: str, consecutive_failures: int) -> bool:
        """Determine if we should switch to a different center"""
        center = self.get_center_by_name(current_center_name)
        if not center:
            return True
        
        # Switch conditions
        max_attempts = self.config["max_attempts_per_center"]
        
        # Give priority 1 center extra attempts
        if center.priority == 1:
            max_attempts += self.config["preferred_center_bonus_attempts"]
        
        if consecutive_failures >= max_attempts:
            self.emit_update(f"🔄 Switching from {current_center_name} after {consecutive_failures} failures")
            self.session_stats["total_center_switches"] += 1
            return True
        
        return False
    
    def get_center_targeting_strategy(self) -> Dict:
        """Get the current center targeting strategy for the booking attempt"""
        # Select next target center
        target_center = self.get_next_target_center()
        
        if not target_center:
            self.emit_update("❌ No available centers to target", "error")
            return None
        
        self.session_stats["current_target_center"] = target_center.name
        self.session_stats["centers_attempted"].append(target_center.name)
        
        strategy = {
            "target_center": target_center.name,
            "priority": target_center.priority,
            "max_attempts": self.config["max_attempts_per_center"],
            "success_rate": target_center.success_rate,
            "estimated_response_time": target_center.average_response_time or 3.0,
            "is_peak_hour": time.localtime().tm_hour in target_center.best_booking_hours
        }
        
        # Give priority 1 center extra attempts
        if target_center.priority == 1:
            strategy["max_attempts"] += self.config["preferred_center_bonus_attempts"]
        
        self.emit_update(f"🎯 Targeting: {target_center.name} (Priority {target_center.priority})")
        return strategy
    
    def validate_center_assignment(self, page_source: str, expected_center: str) -> Tuple[bool, str]:
        """Validate that the booking was assigned to the expected center"""
        try:
            page_lower = page_source.lower()
            expected_lower = expected_center.lower()
            
            # Check for center name variations in confirmation
            center_indicators = [
                expected_lower,
                expected_lower.replace("ltd", "").strip(),
                expected_lower.replace("diagnostics", "").strip(),
                expected_lower.split()[0]  # First word
            ]
            
            for indicator in center_indicators:
                if indicator in page_lower:
                    return True, f"Confirmed booking at {expected_center}"
            
            # Check for any of our preferred centers in the response
            for center in self.preferred_centers:
                center_name_lower = center.name.lower()
                if center_name_lower in page_lower:
                    if center.name != expected_center:
                        return True, f"Booking assigned to {center.name} (different from target)"
                    else:
                        return True, f"Confirmed booking at {center.name}"
            
            return False, "Could not confirm center assignment"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def get_centers_status_summary(self) -> Dict:
        """Get summary of all centers' current status"""
        summary = {}
        for center in self.preferred_centers:
            summary[center.name] = {
                "priority": center.priority,
                "success_rate": f"{center.success_rate:.1f}%",
                "attempts": center.attempt_count,
                "successes": center.success_count,
                "status": center.status.value,
                "last_success": center.last_success_time or "Never",
                "avg_response_time": f"{center.average_response_time:.2f}s"
            }
        return summary
    
    def get_center_analytics(self) -> Dict:
        """Get detailed analytics for center performance"""
        analytics = {
            "total_centers": len(self.preferred_centers),
            "centers_attempted_this_session": len(set(self.session_stats["centers_attempted"])),
            "successful_center": self.session_stats.get("successful_center"),
            "total_center_switches": self.session_stats["total_center_switches"],
            "center_performance": []
        }
        
        for center in sorted(self.preferred_centers, key=lambda x: x.priority):
            perf = {
                "name": center.name,
                "priority": center.priority,
                "success_rate": center.success_rate,
                "total_attempts": center.attempt_count,
                "total_successes": center.success_count,
                "best_hours": center.best_booking_hours,
                "current_status": center.status.value,
                "avg_response_time": center.average_response_time
            }
            analytics["center_performance"].append(perf)
        
        return analytics
    
    def reset_session_stats(self):
        """Reset session-specific statistics"""
        self.session_stats = {
            "centers_attempted": [],
            "current_target_center": None,
            "successful_center": None,
            "total_center_switches": 0
        }
        self.emit_update("🔄 Session statistics reset")
    
    def update_center_list(self, new_centers: List[Dict]):
        """Update the list of preferred centers"""
        self.preferred_centers = []
        
        for i, center_data in enumerate(new_centers, 1):
            center = PreferredCenter(
                name=center_data["name"],
                priority=i
            )
            self.preferred_centers.append(center)
        
        self.emit_update(f"✅ Updated to {len(new_centers)} preferred centers")
        return self.get_centers_status_summary()