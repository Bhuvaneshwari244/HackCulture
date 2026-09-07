"""
AI-Powered Credit Scoring Engine using Alternative Data
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import joblib
import os

class CreditScoringEngine:
    def __init__(self):
        """Initialize credit scoring model"""
        self.model = None
        self.load_or_train_model()
        
    def load_or_train_model(self):
        """Load pretrained model or train new one"""
        model_path = 'models/credit_scoring_model.pkl'
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            # Train a simple model for demo (in production, use real training data)
            self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
            # Dummy training for demo
            X_train = np.random.rand(1000, 10)
            y_train = np.random.randint(0, 2, 1000)
            self.model.fit(X_train, y_train)
    
    def calculate_score(self, data):
        """
        Calculate credit score based on alternative data
        
        Parameters:
        - mobile_usage_months: Number of months using mobile
        - utility_payment_history: List of payment records
        - farming_experience_years: Years of farming experience
        - land_size_acres: Size of farmland
        - annual_income: Annual income in INR
        - education_level: Education level
        - has_smartphone: Boolean
        - distance_to_bank_km: Distance to nearest bank
        - household_size: Number of family members
        """
        
        # Extract features
        mobile_usage = data.get('mobile_usage_months', 0)
        utility_history = data.get('utility_payment_history', [])
        farming_exp = data.get('farming_experience_years', 0)
        land_size = data.get('land_size_acres', 0)
        annual_income = data.get('annual_income', 0)
        education = data.get('education_level', 'primary')
        has_smartphone = data.get('has_smartphone', False)
        distance_to_bank = data.get('distance_to_bank_km', 0)
        household_size = data.get('household_size', 1)
        
        # Calculate component scores
        
        # 1. Mobile Usage Score (0-150)
        mobile_score = min(mobile_usage * 3, 150)
        
        # 2. Utility Payment Score (0-200)
        if utility_history:
            payment_rate = sum(utility_history) / len(utility_history)
            utility_score = payment_rate * 200
        else:
            utility_score = 100  # Neutral score if no history
        
        # 3. Farming Experience Score (0-150)
        farming_score = min(farming_exp * 10, 150)
        
        # 4. Asset Score (0-150)
        asset_score = min((land_size * 20), 150)
        
        # 5. Income Score (0-150)
        income_score = min((annual_income / 1000), 150)
        
        # 6. Digital Literacy Score (0-100)
        digital_score = 100 if has_smartphone else 50
        
        # 7. Banking Accessibility Score (0-100)
        accessibility_score = max(100 - (distance_to_bank * 5), 0)
        
        # Education multiplier (0.8 to 1.2)
        education_multiplier = {
            'none': 0.85,
            'primary': 0.9,
            'secondary': 1.0,
            'higher_secondary': 1.1,
            'graduate': 1.2
        }.get(education, 1.0)
        
        # Calculate final score (300-900 range)
        raw_score = (
            mobile_score +
            utility_score +
            farming_score +
            asset_score +
            income_score +
            digital_score +
            accessibility_score
        )
        
        # Apply education multiplier and normalize to 300-900 range
        final_score = int(300 + (raw_score * education_multiplier * 600 / 1000))
        final_score = max(300, min(900, final_score))
        
        # Determine risk category
        if final_score >= 750:
            risk_category = 'Low Risk'
            approval_likelihood = 'Very High'
        elif final_score >= 650:
            risk_category = 'Medium-Low Risk'
            approval_likelihood = 'High'
        elif final_score >= 550:
            risk_category = 'Medium Risk'
            approval_likelihood = 'Moderate'
        elif final_score >= 450:
            risk_category = 'Medium-High Risk'
            approval_likelihood = 'Low'
        else:
            risk_category = 'High Risk'
            approval_likelihood = 'Very Low'
        
        # Generate improvement tips
        improvement_tips = []
        if mobile_score < 100:
            improvement_tips.append("Maintain consistent mobile usage for at least 6 months")
        if utility_score < 150:
            improvement_tips.append("Improve utility payment history - pay all bills on time")
        if not has_smartphone:
            improvement_tips.append("Consider getting a smartphone for better digital access")
        if asset_score < 100:
            improvement_tips.append("Expand farming operations or document all assets")
        
        return {
            'score': final_score,
            'risk_category': risk_category,
            'approval_likelihood': approval_likelihood,
            'component_scores': {
                'mobile_usage': mobile_score,
                'utility_payment': utility_score,
                'farming_experience': farming_score,
                'assets': asset_score,
                'income': income_score,
                'digital_literacy': digital_score,
                'bank_accessibility': accessibility_score
            },
            'improvement_tips': improvement_tips,
            'eligible_for_loan': final_score >= 400
        }
    
    def calculate_interest_rate(self, credit_score):
        """Calculate interest rate based on credit score"""
        if credit_score >= 750:
            return 7.5
        elif credit_score >= 650:
            return 9.0
        elif credit_score >= 550:
            return 11.0
        elif credit_score >= 450:
            return 13.5
        else:
            return 15.0


# Example usage
if __name__ == '__main__':
    engine = CreditScoringEngine()
    
    # Test case 1: Good farmer profile
    test_data_good = {
        'mobile_usage_months': 36,
        'utility_payment_history': [1, 1, 1, 1, 1, 1],
        'farming_experience_years': 15,
        'land_size_acres': 5.0,
        'annual_income': 150000,
        'education_level': 'secondary',
        'has_smartphone': True,
        'distance_to_bank_km': 3,
        'household_size': 5
    }
    
    result = engine.calculate_score(test_data_good)
    print("Good Farmer Profile:")
    print(f"Credit Score: {result['score']}")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Approval Likelihood: {result['approval_likelihood']}")
    print(f"Interest Rate: {engine.calculate_interest_rate(result['score'])}%")
    print()
    
    # Test case 2: New farmer profile
    test_data_new = {
        'mobile_usage_months': 12,
        'utility_payment_history': [1, 1, 0, 1, 1],
        'farming_experience_years': 2,
        'land_size_acres': 2.0,
        'annual_income': 60000,
        'education_level': 'primary',
        'has_smartphone': False,
        'distance_to_bank_km': 8,
        'household_size': 4
    }
    
    result = engine.calculate_score(test_data_new)
    print("New Farmer Profile:")
    print(f"Credit Score: {result['score']}")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Approval Likelihood: {result['approval_likelihood']}")
    print(f"Interest Rate: {engine.calculate_interest_rate(result['score'])}%")
    print(f"Improvement Tips: {result['improvement_tips']}")
