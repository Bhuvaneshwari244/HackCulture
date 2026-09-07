import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLanguage } from '../App';

const API_URL = 'http://localhost:5000/api';

function Dashboard({ user }) {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userLocation, setUserLocation] = useState(null);
  const { t } = useLanguage();

  useEffect(() => {
    setDashboardData(getMockData());
    setLoading(false);
    
    if (navigator.geolocation) {
      const timeoutId = setTimeout(() => {
        fetchDashboardData(null);
      }, 3000);
      
      navigator.geolocation.getCurrentPosition(
        (position) => {
          clearTimeout(timeoutId);
          const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          setUserLocation(location);
          fetchDashboardData(location);
        },
        () => {
          clearTimeout(timeoutId);
          fetchDashboardData(null);
        },
        { timeout: 3000, maximumAge: 300000 }
      );
    } else {
      fetchDashboardData(null);
    }
  }, [user.id]);

  const fetchDashboardData = async (location) => {
    try {
      const url = location 
        ? `${API_URL}/dashboard/${user.id}?lat=${location.latitude}&lon=${location.longitude}`
        : `${API_URL}/dashboard/${user.id}`;
      
      const response = await axios.get(url, { timeout: 5000 }); // 5 second timeout
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Keep using mock data if API fails
      if (!dashboardData) {
        setDashboardData(getMockData());
      }
    }
  };

  const getMockData = () => ({
    user_id: user.id,
    credit_score: 720,
    active_loans: [
      {
        loan_id: 'LOAN001',
        type: 'Crop Loan',
        amount: 50000,
        outstanding: 35000,
        next_due_date: '2026-08-15',
        next_due_amount: 5000
      }
    ],
    weather_alerts: [
      {
        type: 'rainfall',
        severity: 'moderate',
        message: 'Heavy rainfall expected in next 48 hours'
      }
    ],
    market_prices: {
      wheat: { price: 2150, trend: 'up' },
      rice: { price: 1850, trend: 'stable' },
      cotton: { price: 5600, trend: 'down' }
    },
    financial_literacy_progress: {
      completed_modules: 5,
      total_modules: 10,
      current_streak: 7,
      points: 450
    },
    savings_summary: {
      total_savings: 15000,
      monthly_saving: 2000,
      goal_progress: 0.6
    }
  });

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mb-4"></div>
        <p className="text-gray-600">Loading your dashboard...</p>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-600">No data available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-8">
      {/* Hero Banner - Welcome & Credit Score */}
      <div className="relative bg-gradient-to-r from-green-600 via-emerald-600 to-teal-600 rounded-2xl shadow-2xl overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -mr-32 -mt-32"></div>
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full -ml-24 -mb-24"></div>
        
        <div className="relative z-10 p-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="mb-6 md:mb-0">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
                {t.namaste}, {user.name}! 🙏
              </h1>
              <p className="text-green-50 text-lg">{t.welcomeMsg}</p>
              <div className="flex items-center mt-4 space-x-4">
                <div className="flex items-center text-white/90">
                  <span className="text-2xl mr-2">📍</span>
                  <span>{dashboardData?.current_weather?.location || 'India'}</span>
                </div>
                <div className="flex items-center text-white/90">
                  <span className="text-2xl mr-2">🗓️</span>
                  <span>{new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
                </div>
              </div>
            </div>
            
            {/* Credit Score Highlight */}
            <div className="bg-white/10 backdrop-blur-sm border-2 border-white/20 rounded-2xl p-6 min-w-[200px]">
              <div className="text-center">
                <p className="text-green-50 text-sm font-medium mb-2">{t.creditScore}</p>
                <div className="relative">
                  <div className="text-6xl font-bold text-white">
                    {dashboardData?.credit_score || 720}
                  </div>
                  <div className="absolute -right-2 -top-2 text-3xl">⭐</div>
                </div>
                <p className="text-green-100 text-sm mt-2">{t.excellent}</p>
                <div className="mt-3 h-2 bg-white/20 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-yellow-400 transition-all"
                    style={{ width: `${(dashboardData?.credit_score || 720) / 850 * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon="💰"
          title={t.activeLoans}
          value={dashboardData?.active_loans?.length || 0}
          subtitle={t.inProgress}
          bgColor="bg-blue-500"
          iconBg="bg-blue-400"
        />
        <StatCard
          icon="💵"
          title={t.totalSavings}
          value={`₹${((dashboardData?.savings_summary?.total_savings || 15000) / 1000).toFixed(0)}K`}
          subtitle={`+₹${dashboardData?.savings_summary?.monthly_saving || 2000}/mo`}
          bgColor="bg-purple-500"
          iconBg="bg-purple-400"
        />
        <StatCard
          icon="🎓"
          title={t.learningProgress}
          value={`${dashboardData?.financial_literacy_progress?.completed_modules || 5}/${dashboardData?.financial_literacy_progress?.total_modules || 10}`}
          subtitle={`${dashboardData?.financial_literacy_progress?.points || 450} ${t.points}`}
          bgColor="bg-orange-500"
          iconBg="bg-orange-400"
        />
        <StatCard
          icon="🔥"
          title="Learning Streak"
          value={`${dashboardData?.financial_literacy_progress?.current_streak || 7} days`}
          subtitle="Keep it up!"
          bgColor="bg-red-500"
          iconBg="bg-red-400"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Weather & Market (2/3 width) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Weather Card */}
          <div className="bg-gradient-to-br from-sky-400 to-blue-500 rounded-2xl shadow-xl p-6 text-white">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-2xl font-bold flex items-center">
                <span className="text-3xl mr-3">🌤️</span>
                {t.weatherAlerts}
              </h3>
              {dashboardData?.current_weather?.location && (
                <span className="text-sm bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
                  📍 {dashboardData.current_weather.location}
                </span>
              )}
            </div>

            {dashboardData?.current_weather ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Current Weather */}
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-5">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="text-7xl font-bold">
                        {Math.round(dashboardData.current_weather.temperature)}°
                      </p>
                      {dashboardData.current_weather.feels_like && (
                        <p className="text-sm text-blue-100 mt-1">
                          Feels {Math.round(dashboardData.current_weather.feels_like)}°C
                        </p>
                      )}
                    </div>
                    <div className="text-7xl">
                      {dashboardData.current_weather.temperature > 35 ? '☀️' : 
                       dashboardData.current_weather.temperature > 25 ? '🌤️' : 
                       dashboardData.current_weather.rainfall_probability > 70 ? '🌧️' : '⛅'}
                    </div>
                  </div>
                  {dashboardData.current_weather.description && (
                    <p className="text-blue-100 capitalize font-medium">
                      {dashboardData.current_weather.description}
                    </p>
                  )}
                </div>

                {/* Weather Details */}
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                    <p className="text-blue-100 text-sm mb-1">{t.humidity}</p>
                    <p className="text-3xl font-bold">
                      {dashboardData.current_weather.humidity}%
                    </p>
                  </div>
                  <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                    <p className="text-blue-100 text-sm mb-1">{t.rain}</p>
                    <p className="text-3xl font-bold">
                      {dashboardData.current_weather.rainfall_probability}%
                    </p>
                  </div>
                  {dashboardData.current_weather.wind_speed && (
                    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 col-span-2">
                      <p className="text-blue-100 text-sm mb-1">{t.wind}</p>
                      <p className="text-3xl font-bold">
                        {Math.round(dashboardData.current_weather.wind_speed)} m/s
                      </p>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-blue-100">Loading weather data...</div>
            )}

            {/* Weather Alerts */}
            <div className="mt-5">
              {dashboardData?.weather_alerts && dashboardData.weather_alerts.length > 0 ? (
                dashboardData.weather_alerts.map((alert, index) => (
                  <div key={index} className="bg-yellow-500/90 backdrop-blur-sm rounded-xl p-4 mb-2 border border-yellow-400">
                    <div className="flex items-start">
                      <span className="text-2xl mr-3">⚠️</span>
                      <div>
                        <p className="font-bold text-yellow-900">{alert.message}</p>
                        <p className="text-sm text-yellow-800 mt-1">Severity: {alert.severity}</p>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                  <p className="flex items-center text-green-100">
                    <span className="text-2xl mr-3">✅</span>
                    <span className="font-medium">{t.noActiveAlerts || 'No active weather alerts'}</span>
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Market Prices Card */}
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h3 className="text-2xl font-bold text-gray-800 mb-5 flex items-center">
              <span className="text-3xl mr-3">📈</span>
              {t.marketPrices}
              <span className="ml-auto text-sm font-normal text-gray-500">{t.marketPricesSubtitle}</span>
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(dashboardData?.market_prices || {}).map(([crop, data]) => (
                <div key={crop} className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-5 hover:shadow-lg transition-all">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-4xl">
                      {crop === 'wheat' ? '🌾' : crop === 'rice' ? '�' : '🌿'}
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      data.trend === 'up' ? 'bg-green-500 text-white' : 
                      data.trend === 'down' ? 'bg-red-500 text-white' : 'bg-gray-300 text-gray-700'
                    }`}>
                      {data.trend === 'up' ? '↗ +2.5%' : 
                       data.trend === 'down' ? '↘ -1.2%' : '→ 0%'}
                    </span>
                  </div>
                  <p className="font-bold text-gray-800 capitalize text-lg mb-1">{crop}</p>
                  <p className="text-3xl font-extrabold text-green-700">₹{data.price}</p>
                  <p className="text-sm text-gray-600 mt-1">{t.currentRate}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - Quick Actions & Savings (1/3 width) */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              <span className="text-2xl mr-2">⚡</span>
              {t.quickActionsSec}
            </h3>
            <div className="space-y-3">
              <QuickActionButton icon="💰" text={t.applyLoan} color="green" />
              <QuickActionButton icon="📊" text={t.checkCreditScore} color="blue" />
              <QuickActionButton icon="🎤" text={t.voiceAssistant} color="purple" />
              <QuickActionButton icon="📚" text={t.learnFinance} color="orange" />
            </div>
          </div>

          {/* Savings Goal */}
          <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl shadow-xl p-6 text-white">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <span className="text-2xl mr-2">🎯</span>
              Savings Goal
            </h3>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 mb-4">
              <div className="flex justify-between items-baseline mb-2">
                <span className="text-sm text-purple-100">Current</span>
                <span className="text-2xl font-bold">₹15,000</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-3 mb-2">
                <div 
                  className="bg-yellow-400 h-3 rounded-full transition-all"
                  style={{ width: '60%' }}
                ></div>
              </div>
              <div className="flex justify-between items-baseline">
                <span className="text-sm text-purple-100">Goal</span>
                <span className="text-lg font-bold">₹25,000</span>
              </div>
            </div>
            <p className="text-sm text-purple-100">
              💪 60% complete! ₹10,000 more to reach your goal
            </p>
          </div>
        </div>
      </div>

      {/* Active Loans Section */}
      <div className="bg-white rounded-2xl shadow-xl p-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-5 flex items-center">
          <span className="text-3xl mr-3">💳</span>
          {t.activeLoansSec}
          <span className="ml-auto text-sm font-normal text-gray-500">
            {dashboardData?.active_loans?.length || 0} active
          </span>
        </h3>
        
        {dashboardData?.active_loans?.map((loan) => (
          <div key={loan.loan_id} className="bg-gradient-to-r from-gray-50 to-blue-50 border-2 border-blue-200 rounded-xl p-6 mb-4 hover:shadow-lg transition-all">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
              <div>
                <h4 className="text-2xl font-bold text-gray-800 mb-1">{loan.type}</h4>
                <p className="text-sm text-gray-600">ID: {loan.loan_id}</p>
              </div>
              <span className="mt-3 md:mt-0 bg-green-500 text-white px-5 py-2 rounded-full text-sm font-bold inline-flex items-center w-fit">
                <span className="mr-2">●</span> {t.active}
              </span>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-5">
              <div className="bg-white rounded-lg p-4">
                <p className="text-xs text-gray-600 mb-1">{t.totalAmount}</p>
                <p className="text-2xl font-bold text-gray-800">₹{loan.amount.toLocaleString()}</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <p className="text-xs text-gray-600 mb-1">{t.outstanding}</p>
                <p className="text-2xl font-bold text-orange-600">₹{loan.outstanding.toLocaleString()}</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <p className="text-xs text-gray-600 mb-1">{t.nextDue}</p>
                <p className="text-sm font-bold text-gray-800">{new Date(loan.next_due_date).toLocaleDateString('en-IN')}</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <p className="text-xs text-gray-600 mb-1">{t.dueAmount}</p>
                <p className="text-2xl font-bold text-red-600">₹{loan.next_due_amount.toLocaleString()}</p>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Repayment Progress</span>
                <span className="text-sm font-bold text-green-600">
                  {((loan.amount - loan.outstanding) / loan.amount * 100).toFixed(0)}% {t.paid}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-green-500 to-emerald-500 h-4 rounded-full transition-all shadow-inner flex items-center justify-end pr-2"
                  style={{ width: `${((loan.amount - loan.outstanding) / loan.amount * 100)}%` }}
                >
                  {((loan.amount - loan.outstanding) / loan.amount * 100) > 10 && (
                    <span className="text-xs text-white font-bold">✓</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Stat Card Component (Redesigned)
function StatCard({ icon, title, value, subtitle, bgColor, iconBg }) {
  return (
    <div className={`${bgColor} rounded-xl shadow-lg p-6 text-white transform hover:scale-105 transition-all`}>
      <div className={`${iconBg} w-14 h-14 rounded-full flex items-center justify-center mb-4`}>
        <span className="text-3xl">{icon}</span>
      </div>
      <h3 className="text-sm font-medium text-white/80 mb-1">{title}</h3>
      <p className="text-3xl font-bold mb-1">{value}</p>
      <p className="text-sm text-white/70">{subtitle}</p>
    </div>
  );
}

// Quick Action Button (Redesigned)
function QuickActionButton({ icon, text, color = 'gray' }) {
  const colorClasses = {
    green: 'hover:bg-green-50 hover:border-green-500 hover:text-green-700',
    blue: 'hover:bg-blue-50 hover:border-blue-500 hover:text-blue-700',
    purple: 'hover:bg-purple-50 hover:border-purple-500 hover:text-purple-700',
    orange: 'hover:bg-orange-50 hover:border-orange-500 hover:text-orange-700',
    gray: 'hover:bg-gray-50 hover:border-gray-400'
  };

  return (
    <button className={`w-full flex items-center p-4 bg-white border-2 border-gray-200 rounded-xl transition-all ${colorClasses[color]} group`}>
      <span className="text-3xl mr-3 group-hover:scale-110 transition-transform">{icon}</span>
      <span className="text-sm font-semibold text-gray-700">{text}</span>
      <span className="ml-auto text-gray-400 group-hover:text-current">→</span>
    </button>
  );
}

export default Dashboard;
