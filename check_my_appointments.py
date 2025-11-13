"""
🔍 APPOINTMENT STATUS CHECKER
============================
Check your current bookings and appointment status
"""

import json
from datetime import datetime
from tabulate import tabulate

def check_appointments():
    """Check and display current appointments"""
    
    print("🔍 CHECKING YOUR APPOINTMENTS...")
    print("=" * 50)
    
    # Read appointments database
    try:
        with open('appointments_database.json', 'r') as f:
            data = json.load(f)
            appointments = data.get('appointments', [])
    except FileNotFoundError:
        print("❌ No appointments database found")
        return
    except Exception as e:
        print(f"❌ Error reading appointments: {e}")
        return
    
    if not appointments:
        print("📭 No appointments found in database")
        return
    
    print(f"📊 Found {len(appointments)} appointment(s):")
    print()
    
    # Display appointments in table format
    headers = ["ID", "Name", "Center", "Date", "Time", "Status", "Payment"]
    table_data = []
    
    for apt in appointments:
        table_data.append([
            apt.get('id', 'N/A'),
            apt.get('name', 'N/A'),
            apt.get('center', 'N/A')[:30] + '...' if len(apt.get('center', '')) > 30 else apt.get('center', 'N/A'),
            apt.get('date', 'N/A'),
            apt.get('time', 'N/A'),
            f"✅ {apt.get('status', 'N/A')}" if apt.get('status') == 'Confirmed' else apt.get('status', 'N/A'),
            f"✅ {apt.get('payment_status', 'N/A')}" if apt.get('payment_status') == 'Completed' else apt.get('payment_status', 'N/A')
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Show detailed info for each appointment
    print("\n📋 DETAILED APPOINTMENT INFORMATION:")
    print("=" * 50)
    
    for i, apt in enumerate(appointments, 1):
        print(f"\n🗓️ APPOINTMENT #{i}")
        print("-" * 30)
        print(f"👤 Name: {apt.get('name', 'N/A')}")
        print(f"📧 Email: {apt.get('email', 'N/A')}")
        print(f"🛂 Passport: {apt.get('passport_no', 'N/A')}")
        print(f"🏥 Center: {apt.get('center', 'N/A')}")
        print(f"📅 Date: {apt.get('date', 'N/A')}")
        print(f"⏰ Time: {apt.get('time', 'N/A')}")
        print(f"💰 Amount: ${apt.get('amount', 'N/A')}")
        print(f"📊 Status: {apt.get('status', 'N/A')}")
        print(f"💳 Payment Status: {apt.get('payment_status', 'N/A')}")
        print(f"🆔 Payment ID: {apt.get('payment_id', 'N/A')}")
        print(f"📅 Created: {apt.get('created_at', 'N/A')}")
        
        if apt.get('payment_confirmed_at'):
            print(f"✅ Payment Confirmed: {apt.get('payment_confirmed_at', 'N/A')}")
    
    # Check for confirmation files
    print(f"\n📄 CHECKING CONFIRMATION DOCUMENTS...")
    print("-" * 40)
    
    for apt in appointments:
        name = apt.get('name', '').replace(' ', '_').upper()
        conf_file = f"APPOINTMENT_CONFIRMATION_{name}.txt"
        try:
            with open(conf_file, 'r') as f:
                print(f"✅ Found confirmation: {conf_file}")
        except FileNotFoundError:
            print(f"❌ Missing confirmation: {conf_file}")
    
    print(f"\n🎉 SUMMARY:")
    print("-" * 20)
    confirmed_count = sum(1 for apt in appointments if apt.get('status') == 'Confirmed')
    paid_count = sum(1 for apt in appointments if apt.get('payment_status') == 'Completed')
    print(f"✅ Confirmed Appointments: {confirmed_count}")
    print(f"💳 Paid Appointments: {paid_count}")
    print(f"📊 Total Appointments: {len(appointments)}")

def main():
    print("🚀 APPOINTMENT STATUS CHECKER")
    print("=" * 50)
    print()
    
    check_appointments()
    
    print(f"\n📝 Status check completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
