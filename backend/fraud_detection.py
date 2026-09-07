"""
AI-Powered Fraud Detection System
Real-time anomaly detection for transactions and loan applications
"""

import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import hashlib

class FraudDetector:
    def __init__(self):
        """Initialize fraud detection system"""
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.user_behavior_db = {}  # In production, use actual database
        self.suspicious_patterns = self._load_suspicious_patterns()
        
    def _load_suspicious_patterns(self):
        """Load known suspicious patterns"""
        return {
            'velocity_checks': {
                'max_transactions_per_hour': 10,
                'max_amount_per_day': 100000,
                'max_loan_applications_per_month': 3
            },
            'location_checks': {
                'max_distance_km': 100,  # Max distance from usual location
                'time_threshold_minutes': 30  # Time to travel
            },
            'amount_checks': {
                'unusual_multiplier': 5  # 5x usual transaction amount
            }
        }
    
    def check_transaction(self, data):
        """
        Check transaction for fraud
        
        Parameters:
        - transaction_id: Unique transaction ID
        - user_id: User ID
        - amount: Transaction amount
        - transaction_type: withdrawal, deposit, transfer
        - location: {latitude, longitude}
        - device_id: Device identifier
        - timestamp: ISO datetime
        """
        user_id = data.get('user_id')
        amount = data.get('amount', 0)
        transaction_type = data.get('transaction_type')
        location = data.get('location', {})
        device_id = data.get('device_id')
        timestamp = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
        
        fraud_indicators = []
        risk_score = 0  # 0-100, higher is more suspicious
        
        # Initialize user history if not exists
        if user_id not in self.user_behavior_db:
            self.user_behavior_db[user_id] = {
                'transactions': [],
                'devices': set(),
                'locations': [],
                'average_amount': 0,
                'last_transaction_time': None
            }
        
        user_history = self.user_behavior_db[user_id]
        
        # 1. Velocity Check - Too many transactions
        recent_transactions = [
            t for t in user_history['transactions']
            if (timestamp - t['timestamp']).total_seconds() < 3600
        ]
        
        if len(recent_transactions) > self.suspicious_patterns['velocity_checks']['max_transactions_per_hour']:
            fraud_indicators.append({
                'type': 'High Velocity',
                'severity': 'High',
                'details': f'{len(recent_transactions)} transactions in last hour'
            })
            risk_score += 30
        
        # 2. Amount Check - Unusual amount
        if user_history['average_amount'] > 0:
            amount_ratio = amount / user_history['average_amount']
            if amount_ratio > self.suspicious_patterns['amount_checks']['unusual_multiplier']:
                fraud_indicators.append({
                    'type': 'Unusual Amount',
                    'severity': 'Medium',
                    'details': f'Amount is {amount_ratio:.1f}x usual transaction'
                })
                risk_score += 20
        
        # 3. Location Check - Impossible travel
        if user_history['locations'] and location:
            last_location = user_history['locations'][-1]
            last_time = user_history['last_transaction_time']
            
            if last_time:
                time_diff_minutes = (timestamp - last_time).total_seconds() / 60
                distance_km = self._calculate_distance(
                    last_location['latitude'],
                    last_location['longitude'],
                    location.get('latitude', 0),
                    location.get('longitude', 0)
                )
                
                # Check for impossible travel (>100km in 30 minutes)
                if distance_km > 100 and time_diff_minutes < 30:
                    fraud_indicators.append({
                        'type': 'Impossible Travel',
                        'severity': 'High',
                        'details': f'{distance_km:.0f}km in {time_diff_minutes:.0f} minutes'
                    })
                    risk_score += 40
        
        # 4. Device Check - New device
        if device_id not in user_history['devices']:
            fraud_indicators.append({
                'type': 'New Device',
                'severity': 'Low',
                'details': 'Transaction from unrecognized device'
            })
            risk_score += 10
            user_history['devices'].add(device_id)
        
        # 5. Time Pattern Check - Unusual time
        hour = timestamp.hour
        if hour < 6 or hour > 22:  # Late night transactions
            fraud_indicators.append({
                'type': 'Unusual Time',
                'severity': 'Low',
                'details': f'Transaction at {hour}:00'
            })
            risk_score += 5
        
        # 6. Round Amount Check - Suspiciously round amounts
        if amount >= 1000 and amount % 1000 == 0 and amount > 10000:
            fraud_indicators.append({
                'type': 'Round Amount',
                'severity': 'Low',
                'details': 'Large round amount may indicate automated fraud'
            })
            risk_score += 5
        
        # Update user history
        user_history['transactions'].append({
            'amount': amount,
            'type': transaction_type,
            'timestamp': timestamp,
            'location': location
        })
        
        if location:
            user_history['locations'].append(location)
        
        user_history['last_transaction_time'] = timestamp
        
        # Update average amount
        all_amounts = [t['amount'] for t in user_history['transactions']]
        user_history['average_amount'] = np.mean(all_amounts)
        
        # Determine if fraud
        is_fraud = risk_score >= 50
        
        # Determine action
        if risk_score >= 70:
            action = 'BLOCK'
        elif risk_score >= 50:
            action = 'REVIEW'
        elif risk_score >= 30:
            action = 'FLAG'
        else:
            action = 'ALLOW'
        
        return {
            'transaction_id': data.get('transaction_id'),
            'is_fraud': is_fraud,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'action': action,
            'fraud_indicators': fraud_indicators,
            'recommendation': self._get_recommendation(action, risk_score)
        }
    
    def check_application(self, data):
        """
        Check loan application for fraud
        
        Parameters:
        - Similar to transaction but for loan applications
        """
        user_id = data.get('user_id')
        amount = data.get('amount', 0)
        
        fraud_indicators = []
        risk_score = 0
        
        # 1. Check for duplicate applications
        # In production, check database for duplicate applications
        if self._check_duplicate_application(user_id, amount):
            fraud_indicators.append({
                'type': 'Duplicate Application',
                'severity': 'High',
                'details': 'Similar application found recently'
            })
            risk_score += 40
        
        # 2. Check for suspicious patterns in data
        credit_data = data.get('credit_data', {})
        
        # Too perfect data (all round numbers)
        if self._is_too_perfect(credit_data):
            fraud_indicators.append({
                'type': 'Suspicious Data Pattern',
                'severity': 'Medium',
                'details': 'Data appears fabricated (too many round numbers)'
            })
            risk_score += 25
        
        # 3. Unrealistic income for rural area
        annual_income = credit_data.get('annual_income', 0)
        land_size = credit_data.get('land_size_acres', 0)
        
        if land_size > 0:
            income_per_acre = annual_income / land_size
            if income_per_acre > 100000:  # Unrealistically high
                fraud_indicators.append({
                    'type': 'Unrealistic Income',
                    'severity': 'High',
                    'details': f'Income per acre (₹{income_per_acre:.0f}) seems unrealistic'
                })
                risk_score += 30
        
        is_fraud = risk_score >= 50
        action = 'REVIEW' if is_fraud else 'ALLOW'
        
        return {
            'is_fraud': is_fraud,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'action': action,
            'fraud_indicators': fraud_indicators,
            'recommendation': 'Manual review required' if is_fraud else 'Application can proceed'
        }
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in km
        
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return R * c
    
    def _check_duplicate_application(self, user_id, amount):
        """Check for duplicate loan applications"""
        # Simplified check - in production, query database
        return False
    
    def _is_too_perfect(self, data):
        """Check if data looks fabricated (too many round numbers)"""
        round_count = 0
        total_count = 0
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                total_count += 1
                if value % 1000 == 0 or value % 100 == 0:
                    round_count += 1
        
        if total_count == 0:
            return False
        
        return (round_count / total_count) > 0.7  # More than 70% round numbers
    
    def _get_risk_level(self, risk_score):
        """Convert risk score to risk level"""
        if risk_score < 30:
            return 'Low'
        elif risk_score < 50:
            return 'Medium'
        elif risk_score < 70:
            return 'High'
        else:
            return 'Critical'
    
    def _get_recommendation(self, action, risk_score):
        """Get recommendation based on action"""
        recommendations = {
            'ALLOW': 'Transaction appears legitimate. Proceed.',
            'FLAG': 'Monitor this transaction. May require verification.',
            'REVIEW': 'Hold transaction for manual review by security team.',
            'BLOCK': 'Block transaction immediately. High fraud risk.'
        }
        return recommendations.get(action, 'Review required')


# Example usage
if __name__ == '__main__':
    detector = FraudDetector()
    
    print("Fraud Detection System Demo")
    print("=" * 70)
    
    # Test case 1: Normal transaction
    print("\nTest 1: Normal Transaction")
    normal_tx = {
        'transaction_id': 'TX001',
        'user_id': 'USER123',
        'amount': 5000,
        'transaction_type': 'withdrawal',
        'location': {'latitude': 28.7041, 'longitude': 77.1025},
        'device_id': 'DEVICE_A',
        'timestamp': datetime.now().isoformat()
    }
    
    result = detector.check_transaction(normal_tx)
    print(f"Risk Score: {result['risk_score']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Action: {result['action']}")
    print(f"Is Fraud: {result['is_fraud']}")
    
    # Test case 2: Suspicious transaction (high velocity)
    print("\n\nTest 2: High Velocity Attack")
    for i in range(12):
        suspicious_tx = {
            'transaction_id': f'TX{i:03d}',
            'user_id': 'USER456',
            'amount': 1000,
            'transaction_type': 'transfer',
            'location': {'latitude': 28.7041, 'longitude': 77.1025},
            'device_id': 'DEVICE_B',
            'timestamp': (datetime.now() + timedelta(minutes=i*2)).isoformat()
        }
        result = detector.check_transaction(suspicious_tx)
        if i == 11:  # Show last result
            print(f"After {i+1} transactions in short time:")
            print(f"Risk Score: {result['risk_score']}")
            print(f"Risk Level: {result['risk_level']}")
            print(f"Action: {result['action']}")
            print(f"Fraud Indicators: {len(result['fraud_indicators'])}")
            for indicator in result['fraud_indicators']:
                print(f"  - {indicator['type']}: {indicator['details']}")
