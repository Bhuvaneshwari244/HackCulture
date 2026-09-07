import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function LoanAdvisor({ user }) {
  const [cropData, setCropData] = useState({
    crop_type: 'wheat',
    land_size_acres: 5.0,
    location: {
      latitude: 28.7041,
      longitude: 77.1025,
      district: 'Delhi',
      state: 'Delhi'
    },
    farming_method: 'modern',
    irrigation_available: true,
    previous_yield: 0
  });

  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);

  const crops = ['wheat', 'rice', 'cotton', 'sugarcane', 'maize', 'pulses', 'vegetables'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/crop-loan/recommend`, cropData);
      setRecommendation(response.data);
    } catch (error) {
      console.error('Error getting recommendation:', error);
      // Mock data for demo
      setRecommendation({
        success: true,
        crop_type: cropData.crop_type,
        recommended_amount: 86250,
        breakdown: {
          cultivation_cost: 75000,
          contingency_buffer: 11250,
          cost_per_acre: 15000
        },
        expected_returns: {
          yield_quintals: 100,
          revenue: 215000,
          profit: 140000,
          profit_margin: 65.12
        },
        loan_terms: {
          duration_months: 6,
          interest_rate: 7.0,
          total_repayment: 89269,
          harvest_time: 4
        },
        risk_assessment: {
          overall_risk_score: 35,
          risk_level: 'Low',
          factors: {
            weather_risk: 'Low',
            irrigation_risk: 'Low',
            market_risk: 'rising'
          }
        },
        recommendations: [
          {
            priority: 'Medium',
            category: 'Soil Health',
            recommendation: 'Conduct soil testing before cultivation',
            impact: 'Optimizes fertilizer use and improves yield'
          }
        ]
      });
    }

    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
          <span className="text-3xl mr-3">🌾</span>
          AI Crop Loan Advisor
        </h2>
        <p className="text-gray-600">
          Get personalized loan recommendations based on your crop, land, and market conditions
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-xl font-bold mb-4">Crop Details</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🌾 Select Crop
              </label>
              <select
                value={cropData.crop_type}
                onChange={(e) => setCropData({...cropData, crop_type: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500"
              >
                {crops.map(crop => (
                  <option key={crop} value={crop} className="capitalize">{crop}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🏞️ Land Size (acres)
              </label>
              <input
                type="number"
                step="0.1"
                value={cropData.land_size_acres}
                onChange={(e) => setCropData({...cropData, land_size_acres: parseFloat(e.target.value)})}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🚜 Farming Method
              </label>
              <select
                value={cropData.farming_method}
                onChange={(e) => setCropData({...cropData, farming_method: e.target.value})}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500"
              >
                <option value="traditional">Traditional</option>
                <option value="modern">Modern</option>
                <option value="organic">Organic</option>
              </select>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                checked={cropData.irrigation_available}
                onChange={(e) => setCropData({...cropData, irrigation_available: e.target.checked})}
                className="h-4 w-4 text-green-600 rounded"
              />
              <label className="ml-2 text-sm text-gray-700">
                💧 Irrigation Available
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📊 Previous Yield (quintals) - Optional
              </label>
              <input
                type="number"
                value={cropData.previous_yield}
                onChange={(e) => setCropData({...cropData, previous_yield: parseFloat(e.target.value)})}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white font-bold py-3 rounded-lg hover:from-green-600 hover:to-blue-600 transition-all"
            >
              {loading ? 'Analyzing...' : '🎯 Get Recommendation'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="space-y-4">
          {recommendation ? (
            <>
              {/* Recommended Amount */}
              <div className="bg-gradient-to-br from-green-500 to-blue-500 rounded-xl p-6 text-white">
                <h3 className="text-sm font-medium mb-2">Recommended Loan Amount</h3>
                <div className="text-4xl font-bold mb-4">₹{recommendation.recommended_amount.toLocaleString()}</div>
                <div className="grid grid-cols-3 gap-2 text-sm">
                  <div>
                    <p className="text-green-100">Cultivation</p>
                    <p className="font-bold">₹{(recommendation.breakdown.cultivation_cost / 1000).toFixed(0)}K</p>
                  </div>
                  <div>
                    <p className="text-green-100">Buffer</p>
                    <p className="font-bold">₹{(recommendation.breakdown.contingency_buffer / 1000).toFixed(0)}K</p>
                  </div>
                  <div>
                    <p className="text-green-100">Per Acre</p>
                    <p className="font-bold">₹{(recommendation.breakdown.cost_per_acre / 1000).toFixed(0)}K</p>
                  </div>
                </div>
              </div>

              {/* Expected Returns */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h4 className="font-bold mb-4 flex items-center">
                  <span className="mr-2">📈</span>
                  Expected Returns
                </h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Expected Yield</p>
                    <p className="text-xl font-bold">{recommendation.expected_returns.yield_quintals} quintals</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Revenue</p>
                    <p className="text-xl font-bold text-green-600">₹{recommendation.expected_returns.revenue.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Profit</p>
                    <p className="text-xl font-bold text-blue-600">₹{recommendation.expected_returns.profit.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Profit Margin</p>
                    <p className="text-xl font-bold">{recommendation.expected_returns.profit_margin}%</p>
                  </div>
                </div>
              </div>

              {/* Risk Assessment */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h4 className="font-bold mb-4">⚠️ Risk Assessment</h4>
                <div className={`inline-block px-4 py-2 rounded-full mb-4 ${
                  recommendation.risk_assessment.risk_level === 'Low' ? 'bg-green-100 text-green-800' :
                  recommendation.risk_assessment.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {recommendation.risk_assessment.risk_level} Risk
                </div>
                <div className="space-y-2">
                  {Object.entries(recommendation.risk_assessment.factors).map(([key, value]) => (
                    <div key={key} className="flex justify-between text-sm">
                      <span className="text-gray-600 capitalize">{key.replace(/_/g, ' ')}</span>
                      <span className="font-medium">{value}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              {recommendation.recommendations && recommendation.recommendations.length > 0 && (
                <div className="bg-blue-50 rounded-xl p-4">
                  <h4 className="font-bold mb-3 text-blue-800">💡 Recommendations</h4>
                  <div className="space-y-2">
                    {recommendation.recommendations.map((rec, idx) => (
                      <div key={idx} className="bg-white p-3 rounded-lg">
                        <div className="flex items-start">
                          <span className={`text-xs px-2 py-1 rounded ${
                            rec.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {rec.priority}
                          </span>
                          <div className="ml-3 flex-1">
                            <p className="text-sm font-medium text-gray-800">{rec.recommendation}</p>
                            <p className="text-xs text-gray-600 mt-1">Impact: {rec.impact}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="bg-gray-50 rounded-xl p-12 text-center h-full flex flex-col items-center justify-center">
              <span className="text-6xl mb-4">🌾</span>
              <p className="text-gray-500">Fill the form to get loan recommendations</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default LoanAdvisor;
