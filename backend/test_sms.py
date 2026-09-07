#!/usr/bin/env python3
"""
SMS Testing Script for RuralAI Finance Hub
Test your SMS provider configuration before going live
"""

import os
import sys
from dotenv import load_dotenv
from auth import AuthService

# Load environment variables
load_dotenv()

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def check_provider_config():
    """Check which SMS provider is configured"""
    print_header("📋 Checking SMS Provider Configuration")
    
    providers = []
    
    # Check Twilio
    if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
        providers.append("✅ Twilio")
        print("✅ Twilio: Configured")
        print(f"   - Account SID: {os.getenv('TWILIO_ACCOUNT_SID')[:10]}...")
        print(f"   - Phone Number: {os.getenv('TWILIO_PHONE_NUMBER', 'Not set')}")
    else:
        print("❌ Twilio: Not configured")
    
    # Check MSG91
    if os.getenv('MSG91_AUTH_KEY'):
        providers.append("✅ MSG91")
        print("✅ MSG91: Configured")
        print(f"   - Auth Key: {os.getenv('MSG91_AUTH_KEY')[:10]}...")
    else:
        print("❌ MSG91: Not configured")
    
    # Check Fast2SMS
    if os.getenv('FAST2SMS_API_KEY'):
        providers.append("✅ Fast2SMS")
        print("✅ Fast2SMS: Configured")
        print(f"   - API Key: {os.getenv('FAST2SMS_API_KEY')[:10]}...")
    else:
        print("❌ Fast2SMS: Not configured")
    
    # Check AWS SNS
    if os.getenv('AWS_SNS_REGION'):
        providers.append("✅ AWS SNS")
        print("✅ AWS SNS: Configured")
        print(f"   - Region: {os.getenv('AWS_SNS_REGION')}")
    else:
        print("❌ AWS SNS: Not configured")
    
    if not providers:
        print("\n⚠️  No SMS provider configured - Running in DEMO MODE")
        print("   OTP will only be shown in console")
        print("\n💡 See SMS_SETUP_GUIDE.md for configuration instructions")
    else:
        print(f"\n🎉 Active Providers: {', '.join(providers)}")
    
    return len(providers) > 0

def test_otp_flow():
    """Test complete OTP flow"""
    print_header("🧪 Testing OTP Flow")
    
    # Get phone number
    default_phone = "+919876543210"
    phone = input(f"Enter phone number to test [{default_phone}]: ").strip()
    if not phone:
        phone = default_phone
    
    # Normalize phone number
    if not phone.startswith('+'):
        phone = f'+91{phone.lstrip("0")}'
    
    print(f"\n📱 Testing with phone number: {phone}")
    
    # Initialize auth service
    auth = AuthService()
    
    # Step 1: Request OTP
    print("\n📤 Step 1: Requesting OTP...")
    result = auth.request_otp(phone, 'phone')
    
    if result['success']:
        print("✅ OTP request successful!")
        print(f"   Message: {result['message']}")
        print(f"   Expires in: {result['expires_in']} seconds")
        
        # Step 2: Get OTP from user
        print("\n🔢 Step 2: Enter the OTP received")
        print("   (Check your phone or console for OTP)")
        otp = input("   Enter OTP: ").strip()
        
        if otp:
            # Step 3: Verify OTP
            print("\n🔐 Step 3: Verifying OTP...")
            verify_result = auth.verify_otp(phone, otp)
            
            if verify_result['success']:
                print("✅ OTP verification successful!")
                print(f"   Message: {verify_result['message']}")
                print(f"   User ID: {verify_result['user']['id']}")
                print(f"   Token: {verify_result['token'][:50]}...")
                return True
            else:
                print(f"❌ OTP verification failed: {verify_result['message']}")
                return False
        else:
            print("⚠️  No OTP entered - skipping verification")
            return False
    else:
        print(f"❌ Failed to send OTP: {result['message']}")
        return False

def test_email_otp():
    """Test email OTP flow"""
    print_header("📧 Testing Email OTP Flow")
    
    # Check email config
    if os.getenv('SENDGRID_API_KEY'):
        print("✅ SendGrid configured")
    elif os.getenv('EMAIL_USER'):
        print("✅ Gmail SMTP configured (legacy)")
    else:
        print("⚠️  No email provider configured")
        return False
    
    # Get email
    email = input("Enter email address to test: ").strip()
    
    if not email or '@' not in email:
        print("❌ Invalid email address")
        return False
    
    print(f"\n📧 Testing with email: {email}")
    
    # Initialize auth service
    auth = AuthService()
    
    # Request OTP
    print("\n📤 Sending OTP to email...")
    result = auth.request_otp(email, 'email')
    
    if result['success']:
        print("✅ Email OTP sent successfully!")
        print(f"   Message: {result['message']}")
        return True
    else:
        print(f"❌ Failed to send email: {result['message']}")
        return False

def main():
    """Main test menu"""
    print_header("📱 RuralAI SMS/OTP Testing Tool")
    
    # Check configuration
    has_provider = check_provider_config()
    
    while True:
        print("\n" + "-" * 70)
        print("Choose an option:")
        print("  1. Test SMS OTP Flow (Complete)")
        print("  2. Test Email OTP")
        print("  3. Check Configuration")
        print("  4. View Setup Guide")
        print("  5. Exit")
        print("-" * 70)
        
        choice = input("\nEnter choice [1-5]: ").strip()
        
        if choice == '1':
            test_otp_flow()
        elif choice == '2':
            test_email_otp()
        elif choice == '3':
            check_provider_config()
        elif choice == '4':
            print("\n📖 Opening SMS Setup Guide...")
            print("   See: SMS_SETUP_GUIDE.md")
            os.system("notepad ..\\SMS_SETUP_GUIDE.md")
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted. Goodbye!")
        sys.exit(0)
