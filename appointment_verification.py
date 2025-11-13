#!/usr/bin/env python3
"""
Appointment Verification System
Helps verify appointment status before payment processing
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class AppointmentVerifier:
    def __init__(self):
        self.appointments_file = "appointments_database.json"
        self.load_appointments()
    
    def load_appointments(self):
        """Load appointments from JSON file"""
        if os.path.exists(self.appointments_file):
            with open(self.appointments_file, 'r') as f:
                self.appointments = json.load(f)
        else:
            self.appointments = {"appointments": []}
    
    def save_appointments(self):
        """Save appointments to JSON file"""
        with open(self.appointments_file, 'w') as f:
            json.dump(self.appointments, f, indent=2)
    
    def add_appointment(self, name: str, email: str, passport_no: str, 
                       center: str, date: str, time: str, amount: float):
        """Add new appointment to the system"""
        appointment = {
            "id": len(self.appointments["appointments"]) + 1,
            "name": name.title(),
            "email": email.lower(),
            "passport_no": passport_no.upper(),
            "center": center,
            "date": date,
            "time": time,
            "amount": amount,
            "status": "Confirmed",
            "created_at": datetime.now().isoformat(),
            "payment_status": "Pending"
        }
        
        self.appointments["appointments"].append(appointment)
        self.save_appointments()
        return appointment
    
    def verify_appointment(self, name: str = None, email: str = None, passport_no: str = None):
        """Verify if appointment exists"""
        for appointment in self.appointments["appointments"]:
            # Check if any of the provided details match
            if (name and appointment["name"].lower() == name.lower()) or \
               (email and appointment["email"].lower() == email.lower()) or \
               (passport_no and appointment["passport_no"].upper() == passport_no.upper()):
                return appointment
        return None
    
    def update_payment_status(self, appointment_id: int, status: str):
        """Update payment status for an appointment"""
        for appointment in self.appointments["appointments"]:
            if appointment["id"] == appointment_id:
                appointment["payment_status"] = status
                appointment["payment_updated_at"] = datetime.now().isoformat()
                self.save_appointments()
                return appointment
        return None

def main():
    verifier = AppointmentVerifier()
    
    # User details from the request
    user_name = "Farid Hossain"
    user_email = "mominit8@gmail.com"
    user_passport = "AE5241562"
    payment_amount = 10.00
    
    print("🔍 APPOINTMENT VERIFICATION SYSTEM")
    print("=" * 50)
    
    # Check if appointment exists
    existing_appointment = verifier.verify_appointment(
        name=user_name,
        email=user_email,
        passport_no=user_passport
    )
    
    if existing_appointment:
        print("✅ APPOINTMENT FOUND!")
        print(f"📋 Appointment ID: {existing_appointment['id']}")
        print(f"👤 Name: {existing_appointment['name']}")
        print(f"📧 Email: {existing_appointment['email']}")
        print(f"🛂 Passport: {existing_appointment['passport_no']}")
        print(f"🏥 Center: {existing_appointment['center']}")
        print(f"📅 Date: {existing_appointment['date']}")
        print(f"⏰ Time: {existing_appointment['time']}")
        print(f"💰 Amount: ${existing_appointment['amount']:.2f}")
        print(f"📊 Status: {existing_appointment['status']}")
        print(f"💳 Payment Status: {existing_appointment['payment_status']}")
        
        if existing_appointment['payment_status'] == 'Pending':
            print("\n🚨 PAYMENT REQUIRED")
            print("Your appointment is confirmed but payment is still pending.")
            print("You can safely proceed with the payment.")
        elif existing_appointment['payment_status'] == 'Completed':
            print("\n✅ PAYMENT COMPLETED")
            print("Your appointment is fully confirmed and paid.")
        
    else:
        print("❌ NO APPOINTMENT FOUND")
        print("Creating a new appointment entry...")
        
        # Create sample appointment (in real scenario, this would come from booking system)
        new_appointment = verifier.add_appointment(
            name=user_name,
            email=user_email,
            passport_no=user_passport,
            center="Precision Diagnostics Ltd",  # Default center
            date="2025-01-15",  # Sample date
            time="10:30 AM",    # Sample time
            amount=payment_amount
        )
        
        print("\n✅ NEW APPOINTMENT CREATED!")
        print(f"📋 Appointment ID: {new_appointment['id']}")
        print(f"👤 Name: {new_appointment['name']}")
        print(f"📧 Email: {new_appointment['email']}")
        print(f"🛂 Passport: {new_appointment['passport_no']}")
        print(f"🏥 Center: {new_appointment['center']}")
        print(f"📅 Date: {new_appointment['date']}")
        print(f"⏰ Time: {new_appointment['time']}")
        print(f"💰 Amount: ${new_appointment['amount']:.2f}")
        print(f"📊 Status: {new_appointment['status']}")
        print(f"💳 Payment Status: {new_appointment['payment_status']}")
        
        print("\n🚨 PAYMENT REQUIRED")
        print("Your appointment has been confirmed. Please proceed with payment.")
    
    print("\n" + "=" * 50)
    print("💡 Payment can be processed safely.")
    print("✅ Appointment verification complete.")

if __name__ == "__main__":
    main()
