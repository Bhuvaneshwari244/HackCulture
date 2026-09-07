import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import './App.css';
import { translations } from './translations';
import axios from 'axios';

// Import components
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import CreditScore from './components/CreditScore';
import LoanAdvisor from './components/LoanAdvisor';
import VoiceAssistant from './components/VoiceAssistant';
import Chatbot from './components/Chatbot';
import LearningModules from './components/LearningModules';

// Language Context
const LanguageContext = createContext();

export const useLanguage = () => useContext(LanguageContext);

const API_URL = 'http://localhost:5000/api';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [sidebarHidden, setSidebarHidden] = useState(false);
  const [language, setLanguage] = useState('en');

  // Check for existing session on mount
  useEffect(() => {
    const checkSession = async () => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        try {
          const response = await axios.get(`${API_URL}/auth/verify-token`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          if (response.data.valid) {
            // Token is valid, get user data from token or use stored data
            const storedUser = localStorage.getItem('user_data');
            if (storedUser) {
              setUser(JSON.parse(storedUser));
            }
          } else {
            // Token invalid, clear storage
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_data');
          }
        } catch (err) {
          // Token verification failed, clear storage
          localStorage.removeItem('auth_token');
          localStorage.removeItem('user_data');
        }
      }
      setLoading(false);
    };
    
    checkSession();
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    // Store user data for session persistence
    localStorage.setItem('user_data', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
  };

  // Show loading screen while checking session
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🌾</div>
          <div className="text-xl font-semibold text-gray-700">Loading RuralAI...</div>
        </div>
      </div>
    );
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t: translations[language] }}>
      <Router>
        {!user ? (
          <Login onLogin={handleLogin} />
        ) : (
          <AppLayout 
            user={user} 
            onLogout={handleLogout}
            sidebarCollapsed={sidebarCollapsed} 
            setSidebarCollapsed={setSidebarCollapsed}
            sidebarHidden={sidebarHidden}
            setSidebarHidden={setSidebarHidden}
          />
        )}
      </Router>
    </LanguageContext.Provider>
  );
}

function AppLayout({ user, onLogout, sidebarCollapsed, setSidebarCollapsed, sidebarHidden, setSidebarHidden }) {
  const location = useLocation();
  const { language, setLanguage, t } = useLanguage();

  return (
    <div className="App min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden">
      {/* Animated Weather-Themed Background */}
      <div className="floating-particles">
        {/* Floating Clouds */}
        <div className="absolute top-10 animate-cloud" style={{ left: '-10%', animationDelay: '0s' }}>
          <span className="text-6xl opacity-30">☁️</span>
        </div>
        <div className="absolute top-32 animate-cloud" style={{ left: '-10%', animationDelay: '5s' }}>
          <span className="text-5xl opacity-40">☁️</span>
        </div>
        <div className="absolute top-20 animate-cloud" style={{ left: '-10%', animationDelay: '8s' }}>
          <span className="text-7xl opacity-25">☁️</span>
        </div>
        
        {/* Floating Weather Icons */}
        <div className="absolute top-1/4 animate-float-slow" style={{ left: '10%', animationDelay: '0s' }}>
          <span className="text-4xl">🌤️</span>
        </div>
        <div className="absolute top-1/3 animate-float-slow" style={{ left: '70%', animationDelay: '2s' }}>
          <span className="text-4xl">🌾</span>
        </div>
        <div className="absolute top-2/3 animate-float-slow" style={{ left: '20%', animationDelay: '4s' }}>
          <span className="text-4xl">💧</span>
        </div>
        <div className="absolute top-1/2 animate-float-slow" style={{ left: '80%', animationDelay: '1s' }}>
          <span className="text-4xl">🌻</span>
        </div>
        <div className="absolute bottom-1/4 animate-float-slow" style={{ left: '40%', animationDelay: '3s' }}>
          <span className="text-4xl">🌱</span>
        </div>
        
        {/* Sparkles */}
        <div className="absolute top-20 animate-sparkle" style={{ left: '30%', animationDelay: '0s' }}>
          <span className="text-2xl">✨</span>
        </div>
        <div className="absolute top-40 animate-sparkle" style={{ left: '60%', animationDelay: '1s' }}>
          <span className="text-2xl">✨</span>
        </div>
      </div>

      <div className="flex h-screen">
        {/* Left Sidebar */}
        <aside className={`fixed left-0 top-0 h-full bg-white bg-opacity-95 backdrop-blur-lg shadow-2xl z-50 transition-all duration-300 ${
          sidebarHidden ? '-translate-x-full' : 'translate-x-0'
        } ${sidebarCollapsed ? 'w-20' : 'w-64'}`}>
          {/* Logo Section */}
          <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
            <div className="flex items-center justify-between">
              {!sidebarCollapsed && (
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-3xl">🌾</span>
                    <h1 className="text-xl font-bold">{t.appName}</h1>
                  </div>
                  <p className="text-xs text-blue-100 mt-1">{t.tagline}</p>
                </div>
              )}
              {sidebarCollapsed && (
                <span className="text-3xl mx-auto block">🌾</span>
              )}
            </div>
          </div>

          {/* User Profile */}
          {!sidebarCollapsed && (
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                  {user.name ? user.name.charAt(0) : user.phone.slice(-2)}
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-gray-800">{user.name || 'User'}</p>
                  <p className="text-xs text-gray-500">{user.phone}</p>
                </div>
              </div>
            </div>
          )}

          {/* Navigation Menu */}
          <nav className="py-4 flex-1 overflow-y-auto">
            <SidebarLink 
              to="/" 
              icon="🏠" 
              text={t.dashboard} 
              collapsed={sidebarCollapsed}
              active={location.pathname === '/'}
            />
            <SidebarLink 
              to="/credit-score" 
              icon="📊" 
              text={t.creditScore} 
              collapsed={sidebarCollapsed}
              active={location.pathname === '/credit-score'}
            />
            <SidebarLink 
              to="/loan-advisor" 
              icon="💰" 
              text={t.loanAdvisor} 
              collapsed={sidebarCollapsed}
              active={location.pathname === '/loan-advisor'}
            />
            <SidebarLink 
              to="/voice" 
              icon="🎤" 
              text={t.voiceAssistant} 
              collapsed={sidebarCollapsed}
              active={location.pathname === '/voice'}
            />
            <SidebarLink 
              to="/learn" 
              icon="📚" 
              text={t.learning} 
              collapsed={sidebarCollapsed}
              active={location.pathname === '/learn'}
            />
            <SidebarLink 
              to="/chatbot" 
              icon="💬" 
              text={t.helpSupport} 
              collapsed={sidebarCollapsed}
              active={location.pathname === '/chatbot'}
            />

            {/* Divider */}
            <div className="my-4 mx-4 border-t border-gray-200"></div>

            {/* Additional Links */}
            {!sidebarCollapsed && (
              <div className="px-4 mt-6">
                <p className="text-xs font-semibold text-gray-500 uppercase mb-2">{t.quickActions}</p>
                <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 rounded-lg transition-all flex items-center space-x-2">
                  <span>⚡</span>
                  <span>{t.applyLoan}</span>
                </button>
                <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 rounded-lg transition-all flex items-center space-x-2">
                  <span>📞</span>
                  <span>{t.contactSupport}</span>
                </button>
                <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-blue-50 rounded-lg transition-all flex items-center space-x-2">
                  <span>⚙️</span>
                  <span>Settings</span>
                </button>
              </div>
            )}
          </nav>

          {/* Collapse Button */}
          <div className="p-4 border-t border-gray-200">
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="w-full py-2 px-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-all text-gray-700 text-sm font-medium"
            >
              {sidebarCollapsed ? '→' : '← Collapse'}
            </button>
          </div>
        </aside>

        {/* Main Content Area */}
        <div className={`flex-1 flex flex-col transition-all duration-300 ${
          sidebarHidden ? 'ml-0' : (sidebarCollapsed ? 'ml-20' : 'ml-64')
        }`}>
          {/* Top Header */}
          <header className="bg-white bg-opacity-80 backdrop-blur-md shadow-md relative z-10 border-b border-gray-200">
            <div className="px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  {/* Hamburger Menu Button */}
                  <button
                    onClick={() => setSidebarHidden(!sidebarHidden)}
                    className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-all lg:hidden"
                    title={sidebarHidden ? "Show Sidebar" : "Hide Sidebar"}
                  >
                    <span className="text-2xl">{sidebarHidden ? '☰' : '✕'}</span>
                  </button>
                  
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">
                      {getPageTitle(location.pathname)}
                    </h2>
                    <p className="text-sm text-gray-500 mt-1">
                      {getPageDescription(location.pathname)}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  {/* Language Selector */}
                  <select 
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer shadow-sm"
                  >
                    <option value="en">🇬🇧 English</option>
                    <option value="hi">🇮🇳 हिंदी</option>
                    <option value="te">🇮🇳 తెలుగు</option>
                  </select>
                  
                  {/* Logout Button */}
                  <button
                    onClick={onLogout}
                    className="px-3 py-2 text-sm font-medium text-gray-700 hover:text-red-600 hover:bg-gray-100 rounded-lg transition-all"
                    title="Logout"
                  >
                    🚪 Logout
                  </button>
                  
                  <button className="relative p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-all">
                    <span className="text-2xl">🔔</span>
                    <span className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full"></span>
                  </button>
                  <button className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-all">
                    <span className="text-2xl">⚙️</span>
                  </button>
                </div>
              </div>
            </div>
          </header>

          {/* Page Content */}
          <main className="flex-1 overflow-y-auto p-6 relative z-10">
            <div className="fade-in">
              <Routes>
                <Route path="/" element={<Dashboard user={user} />} />
                <Route path="/credit-score" element={<CreditScore user={user} />} />
                <Route path="/loan-advisor" element={<LoanAdvisor user={user} />} />
                <Route path="/voice" element={<VoiceAssistant user={user} />} />
                <Route path="/learn" element={<LearningModules user={user} />} />
                <Route path="/chatbot" element={<Chatbot user={user} />} />
              </Routes>
            </div>
          </main>

          {/* Footer */}
          <footer className="bg-white bg-opacity-80 backdrop-blur-md border-t border-gray-200 py-4 px-6 relative z-10">
            <div className="flex items-center justify-between text-sm">
              <p className="text-gray-600">
                © 2026 RuralAI Finance Hub | NABARD Hackathon @ GFF 2026
              </p>
              <div className="flex items-center space-x-4">
                <a href="#" className="text-gray-600 hover:text-blue-600 transition-colors">Privacy</a>
                <a href="#" className="text-gray-600 hover:text-blue-600 transition-colors">Terms</a>
                <a href="#" className="text-gray-600 hover:text-blue-600 transition-colors">Help</a>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
}

// Sidebar Link Component
function SidebarLink({ to, icon, text, collapsed, active }) {
  return (
    <Link
      to={to}
      className={`mx-2 my-1 px-4 py-3 flex items-center space-x-3 rounded-lg transition-all ${
        active
          ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
          : 'text-gray-700 hover:bg-blue-50 hover:text-blue-600'
      } ${collapsed ? 'justify-center' : ''}`}
    >
      <span className="text-2xl">{icon}</span>
      {!collapsed && <span className="font-medium">{text}</span>}
    </Link>
  );
}

// Helper functions
function getPageTitle(pathname) {
  const titles = {
    '/': 'Dashboard',
    '/credit-score': 'Credit Score Assessment',
    '/loan-advisor': 'Crop Loan Advisor',
    '/voice': 'Voice Assistant',
    '/learn': 'Financial Literacy',
    '/chatbot': 'Help & Support'
  };
  return titles[pathname] || 'RuralAI Finance Hub';
}

function getPageDescription(pathname) {
  const descriptions = {
    '/': 'Your complete financial overview',
    '/credit-score': 'Check your creditworthiness instantly',
    '/loan-advisor': 'Get personalized loan recommendations',
    '/voice': 'Speak in your language',
    '/learn': 'Learn about banking and finance',
    '/chatbot': 'Get instant help from our AI assistant'
  };
  return descriptions[pathname] || 'Banking for Bharat, powered by AI';
}

export default App;
