import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function CreditScore({ user }) {
  const [formData, setFormData] = useState({
    mobile_usage_months: 24,
    utility_payment_history: [1, 1, 1, 1, 1, 1],
    farming_experience_years: 10,
    land_size_acres: 3.5,
    annual_income: 120000,
    education_level: 'secondary',
    has_smartphone: true,
    distance_to_bank_km: 5,
    household_size: 5
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/credit-score`, {
        user_id: user.id,
        ...formData
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error calculating credit score:', error);
      // Mock result for demo
      setResult({
        score: 680,
        risk_category: 'Medium-Low Risk',
        approval_likelihood: 'High',
        component_scores: {
          mobile_usage: 120,
          utility_payment: 180,
          farming_experience: 100,
          assets: 70,
          income: 120,
          digital_literacy: 100,
          bank_accessibility: 75
        },
        improvement_tips: [
          'Consider getting a smartphone for better digital access',
          'Expand farming operations or document all assets'
        ],
        eligible_for_loan: true
      });
    }

    setLoading(false);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : 
              type === 'number' ? parseFloat(value) : value
    }));
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
          <span className="text-3xl mr-3">📊</span>
          AI-Powered Credit Score
        </h2>
        <p className="text-gray-600 mb-4">
          Get instant credit assessment using alternative data - no traditional credit history needed!
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Your Information</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <InputField
              label="Mobile Usage (months)"
              name="mobile_usage_months"
              type="number"
              value={formData.mobile_usage_months}
              onChange={handleChange}
              icon="📱"
            />

            <InputField
              label="Farming Experience (years)"
              name="farming_experience_years"
              type="number"
              value={formData.farming_experience_years}
              onChange={handleChange}
              icon="🌾"
            />

            <InputField
              label="Land Size (acres)"
              name="land_size_acres"
              type="number"
              step="0.1"
              value={formData.land_size_acres}
              onChange={handleChange}
              icon="🏞️"
            />

            <InputField
              label="Annual Income (₹)"
              name="annual_income"
              type="number"
              value={formData.annual_income}
              onChange={handleChange}
              icon="💰"
            />

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📚 Education Level
              </label>
              <select
                name="education_level"
                value={formData.education_level}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              >
                <option value="none">None</option>
                <option value="primary">Primary</option>
                <option value="secondary">Secondary</option>
                <option value="higher_secondary">Higher Secondary</option>
                <option value="graduate">Graduate</option>
              </select>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                name="has_smartphone"
                checked={formData.has_smartphone}
                onChange={handleChange}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label className="ml-2 block text-sm text-gray-700">
                📱 I have a smartphone
              </label>
            </div>

            <InputField
              label="Distance to Bank (km)"
              name="distance_to_bank_km"
              type="number"
              value={formData.distance_to_bank_km}
              onChange={handleChange}
              icon="🏦"
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white font-bold py-3 px-4 rounded-lg hover:from-green-600 hover:to-blue-600 transition-all disabled:opacity-50"
            >
              {loading ? 'Calculating...' : '🎯 Calculate Credit Score'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div>
          {result ? (
            <div className="space-y-4">
              {/* Score Display */}
              <div className="bg-gradient-to-br from-green-500 to-blue-500 rounded-xl shadow-lg p-8 text-white text-center">
                <h3 className="text-lg font-medium mb-2">Your Credit Score</h3>
                <div className="text-6xl font-bold mb-2">{result.score}</div>
                <div className="inline-block bg-white/20 backdrop-blur px-4 py-2 rounded-full">
                  <p className="text-sm font-medium">{result.risk_category}</p>
                </div>
                <p className="mt-4 text-green-100">
                  Approval Likelihood: <span className="font-bold">{result.approval_likelihood}</span>
                </p>
              </div>

              {/* Component Scores */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <h4 className="font-bold text-gray-800 mb-4">Score Breakdown</h4>
                <div className="space-y-3">
                  {Object.entries(result.component_scores).map(([key, score]) => (
                    <div key={key}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600 capitalize">
                          {key.replace(/_/g, ' ')}
                        </span>
                        <span className="font-medium">{score}/150</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-600 h-2 rounded-full transition-all"
                          style={{ width: `${(score / 150) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Improvement Tips */}
              {result.improvement_tips && result.improvement_tips.length > 0 && (
                <div className="bg-yellow-50 border-l-4 border-yellow-400 rounded-lg p-4">
                  <h4 className="font-bold text-yellow-800 mb-2">💡 Improvement Tips</h4>
                  <ul className="space-y-2">
                    {result.improvement_tips.map((tip, index) => (
                      <li key={index} className="text-sm text-yellow-700 flex items-start">
                        <span className="mr-2">•</span>
                        <span>{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Eligibility */}
              <div className={`rounded-lg p-4 ${
                result.eligible_for_loan 
                  ? 'bg-green-50 border-l-4 border-green-500' 
                  : 'bg-red-50 border-l-4 border-red-500'
              }`}>
                <p className={`font-bold ${result.eligible_for_loan ? 'text-green-800' : 'text-red-800'}`}>
                  {result.eligible_for_loan ? '✅ Eligible for Loan' : '❌ Not Eligible Yet'}
                </p>
              </div>
            </div>
          ) : (
            <div className="bg-gray-50 rounded-xl p-12 text-center h-full flex flex-col items-center justify-center">
              <span className="text-6xl mb-4">📊</span>
              <p className="text-gray-500">Fill the form to calculate your credit score</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function InputField({ label, icon, ...props }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {icon} {label}
      </label>
      <input
        {...props}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
      />
    </div>
  );
}

export default CreditScore;
