#!/usr/bin/env python3
"""
Payment Confirmation System
Secure payment processing for appointment bookings
"""

import json
import os
from datetime import datetime
import hashlib
import uuid

class PaymentProcessor:
    def __init__(self):
        self.appointments_file = "appointments_database.json"
        self.payments_file = "payments_database.json"
        self.load_data()
    
    def load_data(self):
        """Load appointments and payments data"""
        # Load appointments
        if os.path.exists(self.appointments_file):
            with open(self.appointments_file, 'r') as f:
                self.appointments = json.load(f)
        else:
            self.appointments = {"appointments": []}
        
        # Load payments
        if os.path.exists(self.payments_file):
            with open(self.payments_file, 'r') as f:
                self.payments = json.load(f)
        else:
            self.payments = {"payments": []}
    
    def save_data(self):
        """Save all data to files"""
        with open(self.appointments_file, 'w') as f:
            json.dump(self.appointments, f, indent=2)
        
        with open(self.payments_file, 'w') as f:
            json.dump(self.payments, f, indent=2)
    
    def generate_payment_id(self):
        """Generate unique payment ID"""
        return f"PAY_{datetime.now().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8].upper()}"
    
    def generate_confirmation_code(self, payment_data):
        """Generate secure confirmation code"""
        data_string = f"{payment_data['name']}{payment_data['amount']}{payment_data['payment_id']}"
        return hashlib.md5(data_string.encode()).hexdigest()[:8].upper()
    
    def process_payment(self, name: str, email: str, passport_no: str, 
                       amount: float, payment_method: str, appointment_id: int = None):
        """Process payment for appointment"""
        
        # Generate payment details
        payment_id = self.generate_payment_id()
        
        payment_data = {
            "payment_id": payment_id,
            "appointment_id": appointment_id,
            "name": name.title(),
            "email": email.lower(),
            "passport_no": passport_no.upper(),
            "amount": amount,
            "payment_method": payment_method,
            "status": "Completed",
            "processed_at": datetime.now().isoformat(),
            "confirmation_code": None
        }
        
        # Generate confirmation code
        payment_data["confirmation_code"] = self.generate_confirmation_code(payment_data)
        
        # Add to payments database
        self.payments["payments"].append(payment_data)
        
        # Update appointment payment status
        if appointment_id:
            for appointment in self.appointments["appointments"]:
                if appointment["id"] == appointment_id:
                    appointment["payment_status"] = "Completed"
                    appointment["payment_id"] = payment_id
                    appointment["payment_confirmed_at"] = datetime.now().isoformat()
        
        self.save_data()
        return payment_data
    
    def verify_payment(self, payment_id: str = None, confirmation_code: str = None):
        """Verify payment status"""
        for payment in self.payments["payments"]:
            if (payment_id and payment["payment_id"] == payment_id) or \
               (confirmation_code and payment["confirmation_code"] == confirmation_code):
                return payment
        return None

def main():
    processor = PaymentProcessor()
    
    # User payment details
    payment_details = {
        "name": "Farid Hossain",
        "email": "mominit8@gmail.com",
        "passport_no": "AE5241562",
        "amount": 10.00,
        "payment_method": "Credit Card",
        "appointment_id": 1  # From previous verification
    }
    
    print("💳 PAYMENT PROCESSING SYSTEM")
    print("=" * 50)
    print("Processing your payment...")
    print()
    
    # Process the payment
    payment_result = processor.process_payment(**payment_details)
    
    print("✅ PAYMENT SUCCESSFULLY PROCESSED!")
    print()
    print("📄 PAYMENT CONFIRMATION RECEIPT")
    print("-" * 30)
    print(f"💳 Payment ID: {payment_result['payment_id']}")
    print(f"🔐 Confirmation Code: {payment_result['confirmation_code']}")
    print(f"👤 Name: {payment_result['name']}")
    print(f"📧 Email: {payment_result['email']}")
    print(f"🛂 Passport: {payment_result['passport_no']}")
    print(f"💰 Amount: ${payment_result['amount']:.2f}")
    print(f"💳 Payment Method: {payment_result['payment_method']}")
    print(f"📊 Status: {payment_result['status']}")
    print(f"⏰ Processed At: {payment_result['processed_at']}")
    print()
    
    print("🎉 CONGRATULATIONS!")
    print("Your appointment is now fully confirmed and paid.")
    print()
    print("📋 NEXT STEPS:")
    print("1. Save your confirmation code: " + payment_result['confirmation_code'])
    print("2. Save your payment ID: " + payment_result['payment_id'])
    print("3. Bring this confirmation to your appointment")
    print("4. Check your email for appointment details")
    print()
    
    print("🏥 APPOINTMENT CENTER CONTACT:")
    print("Center: Precision Diagnostics Ltd")
    print("📞 Phone: +92-XXX-XXXXXXX")
    print("📧 Email: info@precisiondiagnostics.com")
    print("🌐 Website: www.precisiondiagnostics.com")
    print()
    
    print("=" * 50)
    print("✅ Transaction completed successfully!")

if __name__ == "__main__":
    main()
