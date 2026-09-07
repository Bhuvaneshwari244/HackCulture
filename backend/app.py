"""
RuralAI Finance Hub - Main Backend Application
NABARD Hackathon @ GFF 2026
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

# Import modules
from credit_scoring import CreditScoringEngine
from voice_assistant import VoiceAssistant
from crop_loan_advisor import CropLoanAdvisor
from fraud_detection import FraudDetector
from chatbot import FinancialChatbot
from weather_service import WeatherService
from market_service import MarketService
from auth import AuthService, require_auth
from cashflow_predictor import CashFlowPredictor

app = Flask(__name__)
CORS(app)

# Initialize AI modules
credit_engine = CreditScoringEngine()
voice_assistant = VoiceAssistant()
loan_advisor = CropLoanAdvisor()
fraud_detector = FraudDetector()
chatbot = FinancialChatbot()
weather_service = WeatherService()
market_service = MarketService()
auth_service = AuthService()
cashflow_predictor = CashFlowPredictor()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'RuralAI Finance Hub'
    })

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/request-otp', methods=['POST'])
def request_otp():
    """
    Request OTP for phone number or email
    
    Request body:
    {
        "contact": "+919876543210" or "user@example.com",
        "type": "phone" or "email"
    }
    """
    try:
        data = request.json
        contact = data.get('contact', '').strip()
        contact_type = data.get('type', 'phone')
        
        if not contact:
            return jsonify({'error': 'Contact (phone/email) required'}), 400
        
        result = auth_service.request_otp(contact, contact_type)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP and login
    
    Request body:
    {
        "contact": "+919876543210" or "user@example.com",
        "otp": "123456"
    }
    """
    try:
        data = request.json
        contact = data.get('contact', '').strip()
        otp = data.get('otp', '').strip()
        
        if not contact or not otp:
            return jsonify({'error': 'Contact and OTP required'}), 400
        
        result = auth_service.verify_otp(contact, otp)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify-token', methods=['GET', 'POST'])
def verify_token():
    """
    Verify JWT token
    
    Header: Authorization: Bearer <token>
    OR Request body: { "token": "jwt_token_here" }
    """
    try:
        token = None
        
        # Check Authorization header first (preferred method)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'valid': False, 'error': 'Invalid authorization header'}), 401
        
        # Fallback to request body for backwards compatibility
        if not token and request.json:
            token = request.json.get('token', '')
        
        if not token:
            return jsonify({'valid': False, 'error': 'Token required'}), 400
        
        result = auth_service.verify_token(token)
        
        if result['valid']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

# ==================== PROTECTED ENDPOINTS ====================

@app.route('/api/credit-score', methods=['POST'])
@require_auth
def calculate_credit_score():
    """
    Calculate credit score using alternative data
    
    Request body:
    {
        "user_id": "string",
        "mobile_usage_months": int,
        "utility_payment_history": [1, 1, 1, 0, 1],  # 1=paid, 0=missed
        "farming_experience_years": int,
        "land_size_acres": float,
        "annual_income": float,
        "education_level": "string",
        "has_smartphone": bool,
        "distance_to_bank_km": float,
        "household_size": int
    }
    """
    try:
        data = request.json
        result = credit_engine.calculate_score(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/voice/process', methods=['POST'])
def process_voice():
    """
    Process voice input and return text + audio response
    
    Request: multipart/form-data with audio file
    Form data:
    - audio: audio file
    - language: language code (hi, ta, te, bn, etc.)
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'hi')
        
        result = voice_assistant.process_audio(audio_file, language)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/crop-loan/recommend', methods=['POST'])
def recommend_crop_loan():
    """
    Get crop loan recommendations
    
    Request body:
    {
        "crop_type": "string",
        "land_size_acres": float,
        "location": {
            "latitude": float,
            "longitude": float,
            "district": "string",
            "state": "string"
        },
        "farming_method": "traditional|organic|modern",
        "irrigation_available": bool,
        "previous_yield": float
    }
    """
    try:
        data = request.json
        result = loan_advisor.recommend_loan(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/fraud/check', methods=['POST'])
def check_fraud():
    """
    Check transaction for fraud
    
    Request body:
    {
        "transaction_id": "string",
        "user_id": "string",
        "amount": float,
        "transaction_type": "withdrawal|deposit|transfer",
        "location": {"latitude": float, "longitude": float},
        "device_id": "string",
        "timestamp": "ISO datetime"
    }
    """
    try:
        data = request.json
        result = fraud_detector.check_transaction(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/cashflow/predict', methods=['POST'])
def predict_cashflow():
    """
    Predict cash flow and flag risks for rural micro enterprises
    
    Request body:
    {
        "user_id": "string",
        "business_type": "shop|agriculture|service|manufacturing",
        "monthly_revenue": float,
        "monthly_expenses": float,
        "inventory_value": float,
        "pending_receivables": float,
        "pending_payables": float,
        "seasonal_factor": int (1-10),
        "employee_count": int,
        "loan_obligations": float,
        "cash_in_hand": float,
        "bank_balance": float,
        "credit_sales_ratio": float (0-100),
        "market_conditions": int (1-10),
        "weather_impact": int (1-10),
        "government_scheme_benefit": float
    }
    """
    try:
        data = request.json
        result = cashflow_predictor.predict_cashflow(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    """
    Send message to financial literacy chatbot
    
    Request body:
    {
        "user_id": "string",
        "message": "string",
        "language": "en|hi|ta|te|bn|mr|gu|kn|ml|pa|or",
        "session_id": "string"
    }
    """
    try:
        data = request.json
        result = chatbot.process_message(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/loan/apply', methods=['POST'])
def apply_loan():
    """
    Complete loan application process
    
    Request body:
    {
        "user_id": "string",
        "loan_type": "crop|personal|education|home",
        "amount": float,
        "purpose": "string",
        "duration_months": int,
        "credit_data": {...},
        "crop_data": {...}  # if loan_type is crop
    }
    """
    try:
        data = request.json
        
        # Step 1: Check credit score
        credit_result = credit_engine.calculate_score(data['credit_data'])
        
        if credit_result['score'] < 400:
            return jsonify({
                'approved': False,
                'reason': 'Credit score below minimum threshold',
                'credit_score': credit_result['score'],
                'suggestions': credit_result.get('improvement_tips', [])
            }), 200
        
        # Step 2: Fraud check
        fraud_check = fraud_detector.check_application(data)
        
        if fraud_check['is_fraud']:
            return jsonify({
                'approved': False,
                'reason': 'Application flagged for review',
                'contact_support': True
            }), 200
        
        # Step 3: Calculate loan terms
        if data['loan_type'] == 'crop':
            loan_recommendation = loan_advisor.recommend_loan(data['crop_data'])
            recommended_amount = loan_recommendation['recommended_amount']
        else:
            recommended_amount = data['amount']
        
        # Step 4: Approve loan
        interest_rate = credit_engine.calculate_interest_rate(credit_result['score'])
        
        return jsonify({
            'approved': True,
            'loan_id': f"LOAN{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'approved_amount': recommended_amount,
            'interest_rate': interest_rate,
            'duration_months': data['duration_months'],
            'monthly_emi': calculate_emi(recommended_amount, interest_rate, data['duration_months']),
            'credit_score': credit_result['score'],
            'disbursement_timeline': '24-48 hours'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def calculate_emi(principal, annual_rate, months):
    """Calculate monthly EMI"""
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return principal / months
    emi = principal * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
    return round(emi, 2)

@app.route('/api/dashboard/<user_id>', methods=['GET'])
def get_dashboard_data(user_id):
    """Get complete dashboard data for user with real weather and market data"""
    try:
        # Get location from query parameters (real-time from browser) or use default
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if lat and lon:
            # Use user's current location
            location = {
                'latitude': lat,
                'longitude': lon,
                'district': 'Detecting...',
                'state': ''
            }
            print(f"Using real-time location: {lat}, {lon}")
        else:
            # Fallback to default location
            location = {
                'latitude': 28.7041,
                'longitude': 77.1025,
                'district': 'Delhi',
                'state': 'India'
            }
            print("Using default location: Delhi")
        
        # Get real weather data for the location
        weather_data = weather_service.get_weather_forecast(location)
        
        # Get real market prices
        market_prices = market_service.get_crop_prices()
        
        # Format weather alerts
        weather_alerts = []
        if weather_data.get('alerts'):
            weather_alerts = weather_data['alerts']
        elif weather_data['next_7_days'].get('extreme_weather_alert'):
            weather_alerts.append({
                'type': 'weather',
                'severity': 'moderate',
                'message': 'Extreme weather conditions possible in next 7 days'
            })
        
        # Format market prices
        market_prices_formatted = {}
        for crop, data in market_prices.items():
            market_prices_formatted[crop] = {
                'price': data['price'],
                'trend': data['trend']
            }
        
        # Get location name from weather API response (reverse geocoding)
        location_display = weather_data.get('location_name', location['district'])
        if location_display and location_display != 'Detecting...':
            location_text = f"{location_display}, India"
        else:
            location_text = f"{location['district']}, {location['state']}"
        
        # Extract current weather conditions
        current_weather = {
            'temperature': weather_data['next_7_days']['avg_temperature'],
            'humidity': weather_data['next_7_days']['humidity'],
            'rainfall_probability': weather_data['next_7_days']['rainfall_probability'],
            'condition': weather_data['season_outlook']['overall'],
            'location': location_text
        }
        
        # Add current conditions if available
        if 'current_conditions' in weather_data:
            current_weather.update({
                'temperature': weather_data['current_conditions']['temperature'],
                'feels_like': weather_data['current_conditions']['feels_like'],
                'humidity': weather_data['current_conditions']['humidity'],
                'wind_speed': weather_data['current_conditions']['wind_speed'],
                'description': weather_data['current_conditions']['description']
            })
        
        return jsonify({
            'user_id': user_id,
            'location_detected': bool(lat and lon),
            'coordinates': {'lat': lat, 'lon': lon} if lat and lon else None,
            'credit_score': 720,
            'active_loans': [
                {
                    'loan_id': 'LOAN001',
                    'type': 'Crop Loan',
                    'amount': 50000,
                    'outstanding': 35000,
                    'next_due_date': '2026-08-15',
                    'next_due_amount': 5000
                }
            ],
            'weather_alerts': weather_alerts,
            'weather_source': weather_data.get('source', 'Unknown'),
            'current_weather': current_weather,
            'market_prices': market_prices_formatted,
            'financial_literacy_progress': {
                'completed_modules': 5,
                'total_modules': 10,
                'current_streak': 7,
                'points': 450
            },
            'savings_summary': {
                'total_savings': 15000,
                'monthly_saving': 2000,
                'goal_progress': 0.6
            }
        }), 200
    except Exception as e:
        print(f"Error in dashboard endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
