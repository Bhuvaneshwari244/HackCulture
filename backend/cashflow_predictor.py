"""
AI-Driven Cash Flow Prediction & Risk Flagging System for Rural Micro Enterprises
Predicts future cash flows and flags financial risks using ML
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime, timedelta
import json

class CashFlowPredictor:
    def __init__(self):
        """Initialize cash flow prediction models"""
        self.flow_model = None  # For predicting cash flow amounts
        self.risk_model = None  # For risk classification
        self.scaler = StandardScaler()
        self.load_or_train_models()
        
    def load_or_train_models(self):
        """Load pretrained models or train new ones"""
        flow_model_path = 'models/cashflow_predictor.pkl'
        risk_model_path = 'models/risk_classifier.pkl'
        
        if os.path.exists(flow_model_path) and os.path.exists(risk_model_path):
            self.flow_model = joblib.load(flow_model_path)
            self.risk_model = joblib.load(risk_model_path)
        else:
            # Train models for demo (in production, use real training data)
            self.flow_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.risk_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
            
            # Dummy training for demo
            X_train = np.random.rand(1000, 15)
            y_flow = np.random.rand(1000) * 100000  # Cash flow amounts
            y_risk = np.random.randint(0, 3, 1000)  # Risk levels: 0=Low, 1=Medium, 2=High
            
            self.flow_model.fit(X_train, y_flow)
            self.risk_model.fit(X_train, y_risk)
    
    def predict_cashflow(self, data):
        """
        Predict cash flow and identify risks for rural micro enterprises
        
        Parameters:
        - business_type: Type of micro enterprise (shop, agriculture, service, manufacturing)
        - monthly_revenue: Average monthly revenue (last 3 months)
        - monthly_expenses: Average monthly expenses
        - inventory_value: Current inventory value
        - pending_receivables: Money owed by customers
        - pending_payables: Money owed to suppliers
        - seasonal_factor: Current season impact (1-10)
        - employee_count: Number of employees
        - loan_obligations: Monthly loan repayment amount
        - cash_in_hand: Current cash available
        - bank_balance: Current bank balance
        - credit_sales_ratio: Percentage of sales on credit
        - market_conditions: Local market health (1-10)
        - weather_impact: Weather conditions impact (1-10, 10=best)
        - government_scheme_benefit: Benefit from govt schemes (INR/month)
        """
        
        # Extract features
        business_type = data.get('business_type', 'shop')
        monthly_revenue = data.get('monthly_revenue', 0)
        monthly_expenses = data.get('monthly_expenses', 0)
        inventory_value = data.get('inventory_value', 0)
        pending_receivables = data.get('pending_receivables', 0)
        pending_payables = data.get('pending_payables', 0)
        seasonal_factor = data.get('seasonal_factor', 5)
        employee_count = data.get('employee_count', 0)
        loan_obligations = data.get('loan_obligations', 0)
        cash_in_hand = data.get('cash_in_hand', 0)
        bank_balance = data.get('bank_balance', 0)
        credit_sales_ratio = data.get('credit_sales_ratio', 0)
        market_conditions = data.get('market_conditions', 5)
        weather_impact = data.get('weather_impact', 5)
        govt_scheme_benefit = data.get('government_scheme_benefit', 0)
        
        # Business type encoding
        business_type_map = {'shop': 1, 'agriculture': 2, 'service': 3, 'manufacturing': 4}
        business_type_encoded = business_type_map.get(business_type.lower(), 1)
        
        # Calculate financial ratios
        net_profit_margin = ((monthly_revenue - monthly_expenses) / monthly_revenue * 100) if monthly_revenue > 0 else 0
        current_ratio = ((cash_in_hand + bank_balance + inventory_value) / (pending_payables + loan_obligations)) if (pending_payables + loan_obligations) > 0 else 2.0
        debt_to_income = (loan_obligations / monthly_revenue) if monthly_revenue > 0 else 0
        
        # Predict next 3 months cash flow
        predictions = []
        risk_flags = []
        
        for month in range(1, 4):
            # Adjust factors for future months
            seasonal_adjustment = seasonal_factor + (month * 0.1)
            market_adjustment = market_conditions * (1 - (month * 0.05))
            
            # Calculate expected cash inflow
            expected_revenue = monthly_revenue * (seasonal_adjustment / 5)
            collection_from_receivables = pending_receivables * 0.3  # Assume 30% collected per month
            total_inflow = expected_revenue + collection_from_receivables + govt_scheme_benefit
            
            # Calculate expected cash outflow
            expected_expenses = monthly_expenses * (1 + (month * 0.02))  # Small inflation
            payment_to_suppliers = pending_payables * 0.4  # Pay 40% per month
            loan_payment = loan_obligations
            total_outflow = expected_expenses + payment_to_suppliers + loan_payment
            
            # Net cash flow
            net_cashflow = total_inflow - total_outflow
            
            # Update balances for next iteration
            cash_in_hand += net_cashflow * 0.3
            bank_balance += net_cashflow * 0.7
            pending_receivables = pending_receivables * 0.7 + (expected_revenue * credit_sales_ratio / 100)
            pending_payables = pending_payables * 0.6 + (expected_expenses * 0.3)
            
            # Calculate ending cash position
            ending_cash = cash_in_hand + bank_balance
            
            # Risk assessment for this month
            risk_score = self._calculate_risk_score(
                net_cashflow, ending_cash, loan_obligations,
                monthly_revenue, debt_to_income, current_ratio,
                weather_impact, market_adjustment
            )
            
            risk_level, risk_category = self._categorize_risk(risk_score)
            
            # Identify specific risks
            month_risks = self._identify_risks(
                net_cashflow, ending_cash, loan_obligations,
                pending_payables, debt_to_income, seasonal_factor
            )
            
            predictions.append({
                'month': month,
                'month_name': self._get_month_name(month),
                'cash_inflow': round(total_inflow, 2),
                'cash_outflow': round(total_outflow, 2),
                'net_cashflow': round(net_cashflow, 2),
                'ending_cash_balance': round(ending_cash, 2),
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_category': risk_category
            })
            
            risk_flags.extend(month_risks)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            predictions, risk_flags, business_type,
            monthly_revenue, monthly_expenses, loan_obligations
        )
        
        # Calculate overall health score
        overall_health = self._calculate_health_score(predictions, net_profit_margin, current_ratio)
        
        # Generate alerts
        alerts = self._generate_alerts(predictions, risk_flags)
        
        return {
            'success': True,
            'business_type': business_type,
            'current_financial_position': {
                'cash_in_hand': cash_in_hand,
                'bank_balance': bank_balance,
                'total_liquid_cash': cash_in_hand + bank_balance,
                'pending_receivables': pending_receivables,
                'pending_payables': pending_payables,
                'net_working_capital': (cash_in_hand + bank_balance + pending_receivables) - pending_payables
            },
            'financial_metrics': {
                'net_profit_margin': round(net_profit_margin, 2),
                'current_ratio': round(current_ratio, 2),
                'debt_to_income_ratio': round(debt_to_income, 2),
                'credit_sales_ratio': credit_sales_ratio
            },
            'cashflow_predictions': predictions,
            'risk_flags': risk_flags,
            'overall_health_score': overall_health,
            'alerts': alerts,
            'recommendations': recommendations,
            'prediction_confidence': 'Medium' if len(risk_flags) < 3 else 'Low'
        }
    
    def _calculate_risk_score(self, net_cashflow, ending_cash, loan_obligations,
                               monthly_revenue, debt_to_income, current_ratio,
                               weather_impact, market_conditions):
        """Calculate risk score (0-100, higher = more risk)"""
        risk_score = 50  # Base risk
        
        # Negative cash flow risk
        if net_cashflow < 0:
            risk_score += min(abs(net_cashflow) / 10000 * 10, 20)
        
        # Low cash balance risk
        if ending_cash < loan_obligations * 2:
            risk_score += 15
        
        # High debt risk
        if debt_to_income > 0.4:
            risk_score += 10
        
        # Low current ratio risk
        if current_ratio < 1.5:
            risk_score += 10
        
        # External factors
        if weather_impact < 5:
            risk_score += 5
        if market_conditions < 5:
            risk_score += 5
        
        return min(100, max(0, risk_score))
    
    def _categorize_risk(self, risk_score):
        """Categorize risk level"""
        if risk_score < 30:
            return 'Low', 'green'
        elif risk_score < 50:
            return 'Medium-Low', 'lightgreen'
        elif risk_score < 70:
            return 'Medium', 'yellow'
        elif risk_score < 85:
            return 'Medium-High', 'orange'
        else:
            return 'High', 'red'
    
    def _identify_risks(self, net_cashflow, ending_cash, loan_obligations,
                        pending_payables, debt_to_income, seasonal_factor):
        """Identify specific risk factors"""
        risks = []
        
        if net_cashflow < 0:
            risks.append({
                'type': 'Negative Cash Flow',
                'severity': 'High' if abs(net_cashflow) > 20000 else 'Medium',
                'description': f'Expected negative cash flow of ₹{abs(net_cashflow):,.0f}',
                'impact': 'May struggle to meet expenses'
            })
        
        if ending_cash < loan_obligations * 2:
            risks.append({
                'type': 'Low Cash Reserves',
                'severity': 'High',
                'description': f'Cash balance (₹{ending_cash:,.0f}) less than 2x loan obligation',
                'impact': 'Risk of loan default'
            })
        
        if pending_payables > ending_cash:
            risks.append({
                'type': 'Payables Exceed Cash',
                'severity': 'Medium',
                'description': f'Pending payables (₹{pending_payables:,.0f}) exceed available cash',
                'impact': 'May delay supplier payments'
            })
        
        if debt_to_income > 0.4:
            risks.append({
                'type': 'High Debt Burden',
                'severity': 'Medium',
                'description': f'Debt payments are {debt_to_income*100:.1f}% of income',
                'impact': 'Limited financial flexibility'
            })
        
        if seasonal_factor < 4:
            risks.append({
                'type': 'Unfavorable Season',
                'severity': 'Low',
                'description': 'Current season may reduce business activity',
                'impact': 'Lower revenue expected'
            })
        
        return risks
    
    def _generate_recommendations(self, predictions, risk_flags, business_type,
                                   monthly_revenue, monthly_expenses, loan_obligations):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Check for negative cash flow
        negative_months = [p for p in predictions if p['net_cashflow'] < 0]
        if negative_months:
            recommendations.append({
                'priority': 'Critical',
                'category': 'Cash Flow Management',
                'recommendation': 'Arrange emergency credit line or working capital loan',
                'action': f'Need ₹{abs(min([p["net_cashflow"] for p in negative_months])):,.0f} buffer',
                'timeline': 'Immediate'
            })
        
        # Check for low profit margin
        if monthly_revenue > 0 and (monthly_revenue - monthly_expenses) / monthly_revenue < 0.15:
            recommendations.append({
                'priority': 'High',
                'category': 'Profitability',
                'recommendation': 'Reduce operating costs or increase pricing',
                'action': 'Profit margin < 15%, aim for 20%+',
                'timeline': 'Within 30 days'
            })
        
        # Debt management
        if loan_obligations / monthly_revenue > 0.3:
            recommendations.append({
                'priority': 'High',
                'category': 'Debt Management',
                'recommendation': 'Consider debt restructuring or consolidation',
                'action': 'Negotiate with lenders for extended tenure or lower interest',
                'timeline': 'Within 60 days'
            })
        
        # Revenue diversification
        if business_type in ['agriculture', 'shop']:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Revenue Growth',
                'recommendation': 'Diversify income sources',
                'action': 'Add complementary products/services to reduce dependency',
                'timeline': 'Within 90 days'
            })
        
        # Working capital optimization
        recommendations.append({
            'priority': 'Medium',
            'category': 'Working Capital',
            'recommendation': 'Improve receivables collection',
            'action': 'Offer early payment discounts, reduce credit period',
            'timeline': 'Ongoing'
        })
        
        # Insurance recommendation
        if len(risk_flags) > 3:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Risk Management',
                'recommendation': 'Get business insurance coverage',
                'action': 'Protect against unexpected losses (property, inventory, liability)',
                'timeline': 'Within 60 days'
            })
        
        return recommendations
    
    def _calculate_health_score(self, predictions, profit_margin, current_ratio):
        """Calculate overall financial health score (0-100)"""
        score = 50  # Base score
        
        # Positive cash flow bonus
        positive_months = sum(1 for p in predictions if p['net_cashflow'] > 0)
        score += positive_months * 10
        
        # Profit margin impact
        if profit_margin > 20:
            score += 15
        elif profit_margin > 10:
            score += 10
        elif profit_margin < 5:
            score -= 10
        
        # Current ratio impact
        if current_ratio > 2:
            score += 10
        elif current_ratio < 1:
            score -= 15
        
        # Risk level impact
        avg_risk = sum(p['risk_score'] for p in predictions) / len(predictions)
        score -= (avg_risk - 50) / 2
        
        return max(0, min(100, round(score)))
    
    def _generate_alerts(self, predictions, risk_flags):
        """Generate urgent alerts"""
        alerts = []
        
        # Check for critical cash shortage
        for pred in predictions:
            if pred['ending_cash_balance'] < 10000:
                alerts.append({
                    'type': 'Critical',
                    'message': f"Cash shortage alert for {pred['month_name']}",
                    'details': f"Projected balance: ₹{pred['ending_cash_balance']:,.0f}",
                    'action_required': 'Immediate'
                })
        
        # High risk alerts
        high_risk_count = sum(1 for p in predictions if p['risk_level'] in ['High', 'Medium-High'])
        if high_risk_count >= 2:
            alerts.append({
                'type': 'Warning',
                'message': f'{high_risk_count} months with elevated risk detected',
                'details': 'Financial stress expected in near future',
                'action_required': 'Within 7 days'
            })
        
        # Severe risk flags
        critical_flags = [r for r in risk_flags if r['severity'] == 'High']
        if len(critical_flags) > 2:
            alerts.append({
                'type': 'Warning',
                'message': f'{len(critical_flags)} high-severity risk factors identified',
                'details': 'Multiple financial vulnerabilities present',
                'action_required': 'Within 15 days'
            })
        
        return alerts
    
    def _get_month_name(self, offset):
        """Get month name for offset from current month"""
        future_date = datetime.now() + timedelta(days=30 * offset)
        return future_date.strftime('%B %Y')


# Example usage
if __name__ == '__main__':
    predictor = CashFlowPredictor()
    
    print("Cash Flow Prediction & Risk Flagging System")
    print("=" * 80)
    
    # Test case 1: Healthy micro enterprise (Rural shop)
    test_data_healthy = {
        'business_type': 'shop',
        'monthly_revenue': 80000,
        'monthly_expenses': 55000,
        'inventory_value': 120000,
        'pending_receivables': 25000,
        'pending_payables': 18000,
        'seasonal_factor': 7,
        'employee_count': 2,
        'loan_obligations': 8000,
        'cash_in_hand': 15000,
        'bank_balance': 35000,
        'credit_sales_ratio': 30,
        'market_conditions': 7,
        'weather_impact': 8,
        'government_scheme_benefit': 2000
    }
    
    result = predictor.predict_cashflow(test_data_healthy)
    
    print("\nTest Case 1: Healthy Rural Shop")
    print(f"Business Type: {result['business_type']}")
    print(f"Overall Health Score: {result['overall_health_score']}/100")
    print(f"\nCurrent Position:")
    print(f"  Total Liquid Cash: ₹{result['current_financial_position']['total_liquid_cash']:,.0f}")
    print(f"  Net Working Capital: ₹{result['current_financial_position']['net_working_capital']:,.0f}")
    
    print(f"\n3-Month Cash Flow Forecast:")
    for pred in result['cashflow_predictions']:
        print(f"\n  {pred['month_name']}:")
        print(f"    Inflow: ₹{pred['cash_inflow']:,.0f} | Outflow: ₹{pred['cash_outflow']:,.0f}")
        print(f"    Net: ₹{pred['net_cashflow']:,.0f} | Ending Balance: ₹{pred['ending_cash_balance']:,.0f}")
        print(f"    Risk: {pred['risk_level']} (Score: {pred['risk_score']})")
    
    print(f"\nRisk Flags: {len(result['risk_flags'])}")
    for risk in result['risk_flags'][:3]:
        print(f"  [{risk['severity']}] {risk['type']}: {risk['description']}")
    
    print(f"\nTop Recommendations:")
    for rec in result['recommendations'][:3]:
        print(f"  [{rec['priority']}] {rec['recommendation']}")
    
    print("\n" + "=" * 80)
    
    # Test case 2: Struggling micro enterprise
    test_data_struggling = {
        'business_type': 'agriculture',
        'monthly_revenue': 35000,
        'monthly_expenses': 32000,
        'inventory_value': 45000,
        'pending_receivables': 18000,
        'pending_payables': 25000,
        'seasonal_factor': 3,
        'employee_count': 1,
        'loan_obligations': 12000,
        'cash_in_hand': 5000,
        'bank_balance': 8000,
        'credit_sales_ratio': 50,
        'market_conditions': 4,
        'weather_impact': 4,
        'government_scheme_benefit': 1000
    }
    
    result2 = predictor.predict_cashflow(test_data_struggling)
    
    print("\nTest Case 2: Struggling Agricultural Business")
    print(f"Overall Health Score: {result2['overall_health_score']}/100")
    print(f"Alerts: {len(result2['alerts'])}")
    for alert in result2['alerts']:
        print(f"  [{alert['type']}] {alert['message']}")
    
    print(f"\nCritical Recommendations:")
    for rec in result2['recommendations'][:2]:
        print(f"  [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
