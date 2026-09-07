"""
Authentication Module for RuralAI Finance Hub
Implements OTP-based authentication with SMS
"""

import os
import random
import time
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import jwt
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# In-memory OTP storage (Use Redis in production)
otp_storage = {}
user_sessions = {}

class AuthService:
    """Authentication Service for OTP and JWT management"""
    
    def __init__(self):
        self.sms_api_key = os.getenv('SMS_API_KEY', '')  # Add your SMS provider API key
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY', '')  # SendGrid API key
        self.email_from = os.getenv('EMAIL_FROM', '')  # Verified sender email
        self.email_from_name = os.getenv('EMAIL_FROM_NAME', 'RuralAI Finance Hub')
        # Legacy Gmail (fallback)
        self.email_user = os.getenv('EMAIL_USER', '')  
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
    def generate_otp(self):
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def send_otp_email(self, email, otp):
        """
        Send OTP via Email using SendGrid
        """
        try:
            # Try SendGrid first (preferred method)
            if self.sendgrid_api_key and self.email_from:
                from sendgrid import SendGridAPIClient
                from sendgrid.helpers.mail import Mail, Email, To, Content
                
                # HTML email body
                html_content = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                      <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #10b981; margin: 0;">🌾 RuralAI</h1>
                        <p style="color: #666; margin: 5px 0;">Banking for Bharat</p>
                      </div>
                      
                      <h2 style="color: #333; margin-bottom: 20px;">Your Login OTP</h2>
                      
                      <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0;">
                        <p style="color: white; margin: 0 0 10px 0; font-size: 14px;">Your One-Time Password</p>
                        <h1 style="color: white; font-size: 48px; letter-spacing: 8px; margin: 0;">{otp}</h1>
                      </div>
                      
                      <p style="color: #666; font-size: 14px; margin: 20px 0;">
                        This OTP is valid for <strong>5 minutes</strong>. Please do not share this code with anyone.
                      </p>
                      
                      <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="margin: 0; color: #856404; font-size: 13px;">
                          <strong>⚠️ Security Notice:</strong> RuralAI will never ask for your OTP over phone or email. If you didn't request this OTP, please ignore this email.
                        </p>
                      </div>
                      
                      <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center;">
                        <p style="color: #999; font-size: 12px; margin: 5px 0;">© 2026 RuralAI Finance Hub</p>
                        <p style="color: #999; font-size: 12px; margin: 5px 0;">NABARD Hackathon @ GFF 2026</p>
                      </div>
                    </div>
                  </body>
                </html>
                """
                
                message = Mail(
                    from_email=Email(self.email_from, self.email_from_name),
                    to_emails=To(email),
                    subject=f'Your RuralAI OTP: {otp}',
                    html_content=Content("text/html", html_content)
                )
                
                sg = SendGridAPIClient(self.sendgrid_api_key)
                response = sg.send(message)
                
                print(f"[EMAIL] SendGrid - OTP sent to {email} (Status: {response.status_code})")
                return True
                
            # Fallback to Gmail SMTP (deprecated)
            elif self.email_user and self.email_password:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                
                sender_email = self.email_user
                password = self.email_password
                
                message = MIMEMultipart("alternative")
                message["Subject"] = f"Your RuralAI OTP: {otp}"
                message["From"] = f"RuralAI Finance Hub <{sender_email}>"
                message["To"] = email
                
                html = f"""
                <html>
                  <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px;">
                      <h1 style="color: #10b981;">🌾 RuralAI</h1>
                      <h2>Your Login OTP</h2>
                      <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; text-align: center;">
                        <h1 style="color: white; font-size: 48px; letter-spacing: 8px;">{otp}</h1>
                      </div>
                      <p>This OTP is valid for <strong>5 minutes</strong>.</p>
                    </div>
                  </body>
                </html>
                """
                
                part = MIMEText(html, "html")
                message.attach(part)
                
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, email, message.as_string())
                    print(f"[EMAIL] Gmail SMTP - OTP sent to {email}")
                    return True
            else:
                # Demo mode
                print(f"[EMAIL] Demo Mode - OTP for {email}: {otp}")
                print(f"[EMAIL] Configure SENDGRID_API_KEY in .env to send real emails")
                return True
                
        except Exception as e:
            print(f"[EMAIL] Error sending OTP: {str(e)}")
            return False
    
    def send_otp_sms(self, phone, otp):
        """
        Send OTP via SMS using multiple providers
        Priority: Twilio > MSG91 > Fast2SMS > Demo Mode
        """
        # Normalize phone number (add +91 for Indian numbers if not present)
        if not phone.startswith('+'):
            phone = f'+91{phone.lstrip("0")}'  # Remove leading 0, add +91
        
        try:
            # Method 1: Twilio (International - Most reliable)
            twilio_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
            twilio_token = os.getenv('TWILIO_AUTH_TOKEN', '')
            twilio_from = os.getenv('TWILIO_PHONE_NUMBER', '')
            
            if twilio_sid and twilio_token and twilio_from:
                try:
                    from twilio.rest import Client
                    client = Client(twilio_sid, twilio_token)
                    message = client.messages.create(
                        body=f"Your RuralAI OTP is {otp}. Valid for 5 minutes. Do not share this code with anyone.",
                        from_=twilio_from,
                        to=phone
                    )
                    print(f"✅ [SMS] Twilio - OTP sent to {phone} (SID: {message.sid})")
                    return True
                except Exception as e:
                    print(f"⚠️ [SMS] Twilio failed: {str(e)}")
            
            # Method 2: MSG91 (Indian SMS provider - Affordable)
            msg91_key = os.getenv('MSG91_AUTH_KEY', '')
            msg91_template_id = os.getenv('MSG91_TEMPLATE_ID', '')
            msg91_sender_id = os.getenv('MSG91_SENDER_ID', 'RURALAI')
            
            if msg91_key:
                try:
                    import requests
                    url = "https://api.msg91.com/api/v5/otp"
                    payload = {
                        "template_id": msg91_template_id,
                        "mobile": phone.lstrip('+'),
                        "authkey": msg91_key,
                        "otp": otp,
                        "otp_expiry": "5",  # minutes
                    }
                    headers = {
                        "authkey": msg91_key,
                        "content-type": "application/json"
                    }
                    response = requests.post(url, json=payload, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        print(f"✅ [SMS] MSG91 - OTP sent to {phone}")
                        return True
                    else:
                        print(f"⚠️ [SMS] MSG91 failed: {response.text}")
                except Exception as e:
                    print(f"⚠️ [SMS] MSG91 error: {str(e)}")
            
            # Method 3: Fast2SMS (Indian - Budget friendly)
            fast2sms_key = os.getenv('FAST2SMS_API_KEY', '')
            
            if fast2sms_key:
                try:
                    import requests
                    url = "https://www.fast2sms.com/dev/bulkV2"
                    payload = {
                        "sender_id": "RURALAI",
                        "message": f"Your RuralAI OTP is {otp}. Valid for 5 minutes. Do not share.",
                        "route": "v3",
                        "numbers": phone.lstrip('+91').lstrip('+'),
                    }
                    headers = {
                        "authorization": fast2sms_key,
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Cache-Control": "no-cache"
                    }
                    response = requests.post(url, data=payload, headers=headers, timeout=10)
                    
                    if response.status_code == 200 and response.json().get('return'):
                        print(f"✅ [SMS] Fast2SMS - OTP sent to {phone}")
                        return True
                    else:
                        print(f"⚠️ [SMS] Fast2SMS failed: {response.text}")
                except Exception as e:
                    print(f"⚠️ [SMS] Fast2SMS error: {str(e)}")
            
            # Method 4: AWS SNS (For production scale)
            aws_region = os.getenv('AWS_SNS_REGION', '')
            if aws_region:
                try:
                    import boto3
                    sns_client = boto3.client('sns', region_name=aws_region)
                    response = sns_client.publish(
                        PhoneNumber=phone,
                        Message=f"Your RuralAI OTP is {otp}. Valid for 5 minutes. Do not share this code."
                    )
                    print(f"✅ [SMS] AWS SNS - OTP sent to {phone}")
                    return True
                except Exception as e:
                    print(f"⚠️ [SMS] AWS SNS error: {str(e)}")
            
            # DEMO MODE - Print to console
            print("\n" + "="*60)
            print("🔐 SMS OTP - DEMO MODE")
            print("="*60)
            print(f"📱 Phone: {phone}")
            print(f"🔢 OTP: {otp}")
            print(f"⏰ Valid for: 5 minutes")
            print("="*60)
            print("\n⚙️ To enable real SMS delivery, configure one of:")
            print("   • TWILIO (Recommended): TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER")
            print("   • MSG91 (India): MSG91_AUTH_KEY, MSG91_TEMPLATE_ID")
            print("   • Fast2SMS (India): FAST2SMS_API_KEY")
            print("   • AWS SNS (Enterprise): AWS_SNS_REGION + AWS credentials\n")
            return True
            
        except Exception as e:
            print(f"❌ [SMS] Error: {str(e)}")
            # Still return True in demo mode so app continues to work
            print(f"[SMS] Demo Mode - OTP for {phone}: {otp}")
            return True
    
    def request_otp(self, contact, contact_type='phone'):
        """
        Generate and send OTP to phone or email
        
        Parameters:
        - contact: phone number or email
        - contact_type: 'phone' or 'email'
        
        Returns:
        - success: bool
        - message: str
        """
        # Validate contact
        if contact_type == 'email':
            if not contact or '@' not in contact:
                return {'success': False, 'message': 'Invalid email address'}
        else:
            if not contact or len(contact) < 10:
                return {'success': False, 'message': 'Invalid phone number'}
        
        # Generate OTP
        otp = self.generate_otp()
        
        # Store OTP with expiration (5 minutes)
        otp_storage[contact] = {
            'otp': otp,
            'expires_at': time.time() + 300,  # 5 minutes
            'attempts': 0,
            'type': contact_type
        }
        
        # Send OTP via email or SMS
        if contact_type == 'email':
            sent = self.send_otp_email(contact, otp)
            message = 'OTP sent to your email'
        else:
            sent = self.send_otp_sms(contact, otp)
            message = 'OTP sent to your phone'
        
        if sent:
            return {
                'success': True,
                'message': message,
                'expires_in': 300  # seconds
            }
        else:
            return {
                'success': False,
                'message': 'Failed to send OTP. Please try again.'
            }
    
    def verify_otp(self, contact, otp):
        """
        Verify OTP for phone or email
        
        Returns:
        - success: bool
        - token: JWT token if successful
        - user: user data
        """
        # Check if OTP exists
        if contact not in otp_storage:
            return {'success': False, 'message': 'OTP not found or expired'}
        
        stored_data = otp_storage[contact]
        
        # Check expiration
        if time.time() > stored_data['expires_at']:
            del otp_storage[contact]
            return {'success': False, 'message': 'OTP expired. Please request a new one.'}
        
        # Check attempts (max 3)
        if stored_data['attempts'] >= 3:
            del otp_storage[contact]
            return {'success': False, 'message': 'Too many failed attempts. Please request a new OTP.'}
        
        # Verify OTP
        if stored_data['otp'] != otp:
            stored_data['attempts'] += 1
            return {'success': False, 'message': f'Invalid OTP. {3 - stored_data["attempts"]} attempts remaining.'}
        
        # OTP verified successfully
        del otp_storage[contact]
        
        # Generate JWT token
        token = self.generate_token(contact)
        
        # Get or create user data
        user_data = self.get_or_create_user(contact)
        
        return {
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user_data
        }
    
    def generate_token(self, phone):
        """Generate JWT token for authenticated user"""
        payload = {
            'phone': phone,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return {'valid': True, 'phone': payload['phone']}
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'message': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'message': 'Invalid token'}
    
    def get_or_create_user(self, contact):
        """
        Get user data or create new user
        PRODUCTION: Fetch from database
        """
        # TODO: Replace with database query
        # Example: user = db.users.find_one({'phone': phone})
        
        # Determine if contact is email or phone
        is_email = '@' in contact
        
        user_data = {
            'id': f'USER{hash(contact) % 100000}',
            'phone': contact if not is_email else '',
            'email': contact if is_email else '',
            'name': 'User',  # Get from database or profile
            'language': 'en',
            'created_at': datetime.now().isoformat()
        }
        
        return user_data


# Decorator for protected routes
def require_auth(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Verify token
        auth_service = AuthService()
        result = auth_service.verify_token(token)
        
        if not result['valid']:
            return jsonify({'error': result.get('message', 'Invalid token')}), 401
        
        # Add user info to request
        request.user_phone = result['phone']
        
        return f(*args, **kwargs)
    
    return decorated_function


# Example usage:
if __name__ == '__main__':
    auth = AuthService()
    
    # Test OTP flow
    phone = '+919876543210'
    
    print("=" * 60)
    print("Testing OTP Authentication")
    print("=" * 60)
    
    # Request OTP
    result = auth.request_otp(phone)
    print(f"\n1. Request OTP: {result}")
    
    if result['success']:
        # Get OTP from storage (in production, user enters OTP from SMS)
        otp = otp_storage[phone]['otp']
        print(f"\n2. OTP Generated: {otp}")
        
        # Verify OTP
        verify_result = auth.verify_otp(phone, otp)
        print(f"\n3. Verify OTP: {verify_result}")
        
        if verify_result['success']:
            token = verify_result['token']
            print(f"\n4. JWT Token: {token[:50]}...")
            
            # Verify token
            token_check = auth.verify_token(token)
            print(f"\n5. Token Verification: {token_check}")
    
    print("\n" + "=" * 60)
