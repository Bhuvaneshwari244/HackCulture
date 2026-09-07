"""
AI-Powered Crop Loan Advisor
Integrates weather data, market prices, and ML predictions
"""

import numpy as np
from datetime import datetime, timedelta
import json
from weather_service import WeatherService
from market_service import MarketService

class CropLoanAdvisor:
    def __init__(self):
        """Initialize crop loan advisor with crop database and services"""
        self.crop_data = self._load_crop_database()
        self.weather_service = WeatherService()
        self.market_service = MarketService()
        
    def _load_crop_database(self):
        """Load crop information database"""
        return {
            'wheat': {
                'season': 'rabi',
                'duration_months': 4,
                'cost_per_acre': 15000,
                'expected_yield_quintal': 20,
                'current_price_per_quintal': 2150,
                'water_requirement': 'medium',
                'suitable_soil': ['loamy', 'clay']
            },
            'rice': {
                'season': 'kharif',
                'duration_months': 4,
                'cost_per_acre': 18000,
                'expected_yield_quintal': 25,
                'current_price_per_quintal': 1850,
                'water_requirement': 'high',
                'suitable_soil': ['clay', 'loamy']
            },
            'cotton': {
                'season': 'kharif',
                'duration_months': 6,
                'cost_per_acre': 20000,
                'expected_yield_quintal': 8,
                'current_price_per_quintal': 5600,
                'water_requirement': 'medium',
                'suitable_soil': ['black', 'loamy']
            },
            'sugarcane': {
                'season': 'perennial',
                'duration_months': 12,
                'cost_per_acre': 35000,
                'expected_yield_quintal': 300,
                'current_price_per_quintal': 280,
                'water_requirement': 'very_high',
                'suitable_soil': ['loamy', 'clay']
            },
            'maize': {
                'season': 'kharif',
                'duration_months': 3,
                'cost_per_acre': 12000,
                'expected_yield_quintal': 18,
                'current_price_per_quintal': 1650,
                'water_requirement': 'medium',
                'suitable_soil': ['loamy', 'sandy']
            },
            'pulses': {
                'season': 'rabi',
                'duration_months': 3,
                'cost_per_acre': 10000,
                'expected_yield_quintal': 10,
                'current_price_per_quintal': 4500,
                'water_requirement': 'low',
                'suitable_soil': ['loamy', 'black']
            },
            'vegetables': {
                'season': 'both',
                'duration_months': 2,
                'cost_per_acre': 25000,
                'expected_yield_quintal': 50,
                'current_price_per_quintal': 1200,
                'water_requirement': 'high',
                'suitable_soil': ['loamy', 'sandy']
            }
        }
    
    def recommend_loan(self, data):
        """
        Recommend crop loan based on multiple factors
        
        Parameters:
        - crop_type: Type of crop
        - land_size_acres: Size of land
        - location: Location data (lat, long, district, state)
        - farming_method: traditional, organic, or modern
        - irrigation_available: Boolean
        - previous_yield: Previous yield in quintals
        """
        crop_type = data.get('crop_type', '').lower()
        land_size = data.get('land_size_acres', 0)
        location = data.get('location', {})
        farming_method = data.get('farming_method', 'traditional')
        irrigation_available = data.get('irrigation_available', False)
        previous_yield = data.get('previous_yield', 0)
        
        # Get crop information
        if crop_type not in self.crop_data:
            return {
                'success': False,
                'error': f'Crop type "{crop_type}" not found in database',
                'available_crops': list(self.crop_data.keys())
            }
        
        crop_info = self.crop_data[crop_type]
        
        # Calculate base loan amount
        base_cost_per_acre = crop_info['cost_per_acre']
        
        # Adjust for farming method
        method_multiplier = {
            'traditional': 1.0,
            'organic': 1.3,  # Organic farming costs more
            'modern': 1.2    # Modern equipment costs more
        }.get(farming_method, 1.0)
        
        adjusted_cost_per_acre = base_cost_per_acre * method_multiplier
        
        # Calculate total cultivation cost
        total_cultivation_cost = adjusted_cost_per_acre * land_size
        
        # Add buffer for contingencies (15%)
        contingency_buffer = total_cultivation_cost * 0.15
        
        # Recommended loan amount
        recommended_amount = int(total_cultivation_cost + contingency_buffer)
        
        # Calculate expected returns
        expected_yield = crop_info['expected_yield_quintal'] * land_size
        
        # Adjust yield based on irrigation
        if crop_info['water_requirement'] in ['high', 'very_high'] and not irrigation_available:
            expected_yield *= 0.7  # 30% reduction without irrigation
        
        # Adjust based on previous yield
        if previous_yield > 0:
            yield_ratio = previous_yield / (crop_info['expected_yield_quintal'] * land_size)
            if yield_ratio > 1:
                expected_yield *= min(yield_ratio, 1.3)  # Cap at 30% increase
            else:
                expected_yield *= max(yield_ratio, 0.7)  # Floor at 30% decrease
        
        expected_revenue = expected_yield * crop_info['current_price_per_quintal']
        expected_profit = expected_revenue - total_cultivation_cost
        
        # Get weather forecast
        weather_data = self._get_weather_forecast(location)
        
        # Get market price trend
        price_trend = self._get_price_trend(crop_type)
        
        # Calculate risk factors
        risk_factors = self._calculate_risk_factors(
            crop_info,
            irrigation_available,
            weather_data,
            price_trend
        )
        
        # Loan repayment schedule
        duration_months = crop_info['duration_months'] + 2  # Add 2 months buffer
        interest_rate = 7.0  # Agricultural loan interest rate
        
        # Calculate monthly installment (after harvest)
        total_repayment = recommended_amount * (1 + (interest_rate * duration_months / 12 / 100))
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            crop_type,
            crop_info,
            irrigation_available,
            farming_method,
            risk_factors
        )
        
        return {
            'success': True,
            'crop_type': crop_type,
            'recommended_amount': recommended_amount,
            'breakdown': {
                'cultivation_cost': int(total_cultivation_cost),
                'contingency_buffer': int(contingency_buffer),
                'cost_per_acre': int(adjusted_cost_per_acre)
            },
            'expected_returns': {
                'yield_quintals': round(expected_yield, 2),
                'revenue': int(expected_revenue),
                'profit': int(expected_profit),
                'profit_margin': round((expected_profit / expected_revenue * 100), 2) if expected_revenue > 0 else 0
            },
            'loan_terms': {
                'duration_months': duration_months,
                'interest_rate': interest_rate,
                'total_repayment': int(total_repayment),
                'harvest_time': crop_info['duration_months']
            },
            'risk_assessment': risk_factors,
            'weather_forecast': weather_data,
            'market_trend': price_trend,
            'recommendations': recommendations,
            'timeline': self._generate_timeline(crop_info['duration_months'])
        }
    
    def _get_weather_forecast(self, location):
        """Get weather forecast for location using real API"""
        return self.weather_service.get_weather_forecast(location)
    
    def _get_price_trend(self, crop_type):
        """Get market price trend using real market data"""
        prices = self.market_service.get_crop_prices(crop_type)
        
        if crop_type.lower() in prices:
            crop_data = prices[crop_type.lower()]
            return {
                'current_trend': crop_data['trend'],
                'last_30_days_change': crop_data.get('last_30_days_change', 0),
                'forecast_next_harvest': crop_data['trend'],
                'demand_outlook': crop_data.get('demand_outlook', 'Moderate'),
                'source': crop_data.get('source', 'Market Data')
            }
        
        # Fallback to simulated data
        trends = ['rising', 'stable', 'falling']
        trend = np.random.choice(trends, p=[0.4, 0.4, 0.2])
        
        return {
            'current_trend': trend,
            'last_30_days_change': np.random.uniform(-5, 10),
            'forecast_next_harvest': trend,
            'demand_outlook': 'Strong' if trend == 'rising' else 'Moderate',
            'source': 'Simulated Data'
        }
    
    def _calculate_risk_factors(self, crop_info, irrigation, weather, price_trend):
        """Calculate risk factors"""
        risk_score = 50  # Base risk score (0-100, lower is better)
        
        # Weather risk
        if weather['next_7_days']['extreme_weather_alert']:
            risk_score += 20
        
        # Irrigation risk
        if crop_info['water_requirement'] in ['high', 'very_high'] and not irrigation:
            risk_score += 15
        
        # Market risk
        if price_trend['current_trend'] == 'falling':
            risk_score += 10
        elif price_trend['current_trend'] == 'rising':
            risk_score -= 10
        
        # Determine risk level
        if risk_score < 40:
            risk_level = 'Low'
        elif risk_score < 60:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        return {
            'overall_risk_score': min(100, max(0, risk_score)),
            'risk_level': risk_level,
            'factors': {
                'weather_risk': 'Low' if not weather['next_7_days']['extreme_weather_alert'] else 'High',
                'irrigation_risk': 'Low' if irrigation else 'Medium',
                'market_risk': price_trend['current_trend']
            }
        }
    
    def _generate_recommendations(self, crop_type, crop_info, irrigation, method, risk):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Irrigation recommendation
        if crop_info['water_requirement'] in ['high', 'very_high'] and not irrigation:
            recommendations.append({
                'priority': 'High',
                'category': 'Infrastructure',
                'recommendation': 'Install drip irrigation or ensure reliable water source',
                'impact': 'Can increase yield by 30-40%'
            })
        
        # Insurance recommendation
        if risk['risk_level'] in ['Medium', 'High']:
            recommendations.append({
                'priority': 'High',
                'category': 'Risk Management',
                'recommendation': 'Consider Pradhan Mantri Fasal Bima Yojana (crop insurance)',
                'impact': 'Protects against crop loss'
            })
        
        # Farming method recommendation
        if method == 'traditional':
            recommendations.append({
                'priority': 'Medium',
                'category': 'Efficiency',
                'recommendation': 'Adopt modern farming techniques or organic methods',
                'impact': 'Can increase profit margin by 20-30%'
            })
        
        # Soil testing
        recommendations.append({
            'priority': 'Medium',
            'category': 'Soil Health',
            'recommendation': 'Conduct soil testing before cultivation',
            'impact': 'Optimizes fertilizer use and improves yield'
        })
        
        return recommendations
    
    def _generate_timeline(self, duration_months):
        """Generate cultivation and loan timeline"""
        today = datetime.now()
        
        return {
            'loan_approval': 'Within 48 hours',
            'disbursement': (today + timedelta(days=3)).strftime('%Y-%m-%d'),
            'cultivation_start': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
            'mid_season_review': (today + timedelta(days=duration_months * 15)).strftime('%Y-%m-%d'),
            'expected_harvest': (today + timedelta(days=duration_months * 30)).strftime('%Y-%m-%d'),
            'loan_repayment_due': (today + timedelta(days=(duration_months + 2) * 30)).strftime('%Y-%m-%d')
        }


# Example usage
if __name__ == '__main__':
    advisor = CropLoanAdvisor()
    
    print("Crop Loan Advisor Demo")
    print("=" * 70)
    
    # Test case: Wheat farmer
    test_data = {
        'crop_type': 'wheat',
        'land_size_acres': 5.0,
        'location': {
            'latitude': 28.7041,
            'longitude': 77.1025,
            'district': 'Delhi',
            'state': 'Delhi'
        },
        'farming_method': 'modern',
        'irrigation_available': True,
        'previous_yield': 95
    }
    
    result = advisor.recommend_loan(test_data)
    
    if result['success']:
        print(f"\nCrop: {result['crop_type'].upper()}")
        print(f"Recommended Loan Amount: ₹{result['recommended_amount']:,}")
        print(f"\nExpected Returns:")
        print(f"  Yield: {result['expected_returns']['yield_quintals']} quintals")
        print(f"  Revenue: ₹{result['expected_returns']['revenue']:,}")
        print(f"  Profit: ₹{result['expected_returns']['profit']:,}")
        print(f"  Profit Margin: {result['expected_returns']['profit_margin']}%")
        print(f"\nRisk Assessment: {result['risk_assessment']['risk_level']}")
        print(f"\nTop Recommendations:")
        for rec in result['recommendations'][:3]:
            print(f"  [{rec['priority']}] {rec['recommendation']}")
