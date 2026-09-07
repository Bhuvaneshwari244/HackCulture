import React, { useState } from 'react';
import axios from 'axios';
import { useLanguage } from '../App';

const API_URL = 'http://localhost:5000/api';

function Login({ onLogin }) {
  const [contactType, setContactType] = useState('phone'); // 'phone' or 'email'
  const [contact, setContact] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1); // 1: Enter contact, 2: Enter OTP
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { t } = useLanguage();

  const handleRequestOTP = async (e) => {
    e.preventDefault();
    setError('');
    
    // Validation
    if (contactType === 'email') {
      if (!contact || !contact.includes('@')) {
        setError('Please enter a valid email address');
        return;
      }
    } else {
      if (!contact || contact.length < 10) {
        setError('Please enter a valid 10-digit phone number');
        return;
      }
    }

    setLoading(true);
    
    try {
      const contactValue = contactType === 'phone' ? `+91${contact}` : contact;
      const response = await axios.post(`${API_URL}/auth/request-otp`, {
        contact: contactValue,
        type: contactType
      });
      
      if (response.data.success) {
        setStep(2);
        setError('');
        
        // Show the OTP in console for demo
        console.log(`📱 OTP sent to ${contactValue}`);
        if (contactType === 'phone') {
          alert(`Demo Mode: OTP sent to ${contactValue}\n\nCheck the backend console for the OTP code.`);
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to send OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!otp || otp.length !== 6) {
      setError('Please enter a valid 6-digit OTP');
      return;
    }

    setLoading(true);
    
    try {
      const contactValue = contactType === 'phone' ? `+91${contact}` : contact;
      const response = await axios.post(`${API_URL}/auth/verify-otp`, {
        contact: contactValue,
        otp: otp
      });
      
      if (response.data.success) {
        // Store token
        localStorage.setItem('auth_token', response.data.token);
        
        // Login with user data
        onLogin(response.data.user);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Invalid OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = () => {
    // Quick demo login
    const userData = {
      id: 'USER123',
      name: 'राम कुमार',
      phone: '+91 9876543210',
      language: 'en'
    };
    onLogin(userData);
  };

  const handleBack = () => {
    setStep(1);
    setOtp('');
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden flex items-center justify-center">
      {/* Animated Background */}
      <div className="floating-particles">
        <div className="absolute top-10 animate-cloud" style={{ left: '-10%', animationDelay: '0s' }}>
          <span className="text-6xl opacity-30">☁️</span>
        </div>
        <div className="absolute top-1/4 animate-float-slow" style={{ left: '10%', animationDelay: '0s' }}>
          <span className="text-4xl">🌾</span>
        </div>
        <div className="absolute top-1/3 animate-float-slow" style={{ left: '70%', animationDelay: '2s' }}>
          <span className="text-4xl">🌤️</span>
        </div>
      </div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md mx-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          {/* Logo & Title */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <span className="text-5xl">🌾</span>
              <h1 className="text-3xl font-bold text-gray-800">RuralAI</h1>
            </div>
            <p className="text-gray-600">Banking for Bharat</p>
            <p className="text-sm text-gray-500 mt-2">Digital Banking for Rural India</p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm rounded">
              {error}
            </div>
          )}

          {/* Step 1: Enter Contact (Phone or Email) */}
          {step === 1 && (
            <form onSubmit={handleRequestOTP} className="space-y-4">
              {/* Toggle between Phone and Email */}
              <div className="flex rounded-lg overflow-hidden border border-gray-300">
                <button
                  type="button"
                  onClick={() => setContactType('email')}
                  className={`flex-1 py-2 px-4 font-medium transition-colors ${
                    contactType === 'email'
                      ? 'bg-gradient-to-r from-green-500 to-blue-500 text-white'
                      : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📧 Email
                </button>
                <button
                  type="button"
                  onClick={() => setContactType('phone')}
                  className={`flex-1 py-2 px-4 font-medium transition-colors ${
                    contactType === 'phone'
                      ? 'bg-gradient-to-r from-green-500 to-blue-500 text-white'
                      : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📱 Phone
                </button>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {contactType === 'email' ? 'Email Address' : 'Phone Number'}
                </label>
                
                {contactType === 'email' ? (
                  <input
                    type="email"
                    value={contact}
                    onChange={(e) => setContact(e.target.value)}
                    placeholder="your.email@example.com"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    disabled={loading}
                  />
                ) : (
                  <div className="flex">
                    <span className="inline-flex items-center px-3 py-3 bg-gray-100 border border-r-0 border-gray-300 rounded-l-lg text-gray-700 font-medium">
                      +91
                    </span>
                    <input
                      type="tel"
                      value={contact}
                      onChange={(e) => setContact(e.target.value.replace(/\D/g, '').slice(0, 10))}
                      placeholder="98765 43210"
                      maxLength="10"
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-r-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      disabled={loading}
                    />
                  </div>
                )}
                
                <p className="text-xs text-gray-500 mt-1">
                  {contactType === 'email' 
                    ? 'We\'ll send a 6-digit OTP to your email' 
                    : 'We\'ll send a 6-digit OTP to your phone'}
                </p>
              </div>

              <button
                type="submit"
                disabled={loading || !contact || (contactType === 'phone' && contact.length < 10)}
                className="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Sending OTP...' : 'Send OTP →'}
              </button>
            </form>
          )}

          {/* Step 2: Enter OTP */}
          {step === 2 && (
            <form onSubmit={handleVerifyOTP} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter OTP
                </label>
                <input
                  type="text"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  placeholder="Enter 6-digit OTP"
                  maxLength="6"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-center text-2xl tracking-widest"
                  disabled={loading}
                  autoFocus
                />
                <p className="text-xs text-gray-500 mt-1 text-center">
                  OTP sent to {contactType === 'email' ? contact : `+91 ${contact}`}
                </p>
              </div>

              <button
                type="submit"
                disabled={loading || otp.length !== 6}
                className="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Verifying...' : 'Verify & Login →'}
              </button>

              <button
                type="button"
                onClick={handleBack}
                className="w-full text-gray-600 hover:text-gray-800 text-sm font-medium"
              >
                ← Change {contactType === 'email' ? 'Email' : 'Phone Number'}
              </button>
            </form>
          )}

          {/* Demo Login */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Or</span>
              </div>
            </div>
            
            <button
              onClick={handleDemoLogin}
              className="w-full mt-4 bg-gray-100 text-gray-700 py-3 rounded-lg font-medium hover:bg-gray-200 transition-all"
            >
              🎯 Demo Login (Skip Authentication)
            </button>
          </div>

          {/* Features */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-xs text-gray-500 text-center mb-3">Why RuralAI?</p>
            <div className="space-y-2">
              <div className="flex items-center text-sm text-gray-600">
                <span className="mr-2">✅</span>
                <span>AI-powered credit scoring</span>
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <span className="mr-2">🌤️</span>
                <span>Real-time weather & market data</span>
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <span className="mr-2">🌐</span>
                <span>Multilingual support (हिंदी, తెలుగు)</span>
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <span className="mr-2">🎤</span>
                <span>Voice assistant for farmers</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-600 mt-6">
          © 2026 RuralAI Finance Hub | NABARD Hackathon @ GFF 2026
        </p>
      </div>
    </div>
  );
}

export default Login;
