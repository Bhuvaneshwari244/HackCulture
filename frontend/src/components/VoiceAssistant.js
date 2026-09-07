import React, { useState } from 'react';

function VoiceAssistant({ user }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [language, setLanguage] = useState('hi');

  const languages = [
    { code: 'hi', name: 'हिंदी (Hindi)', flag: '🇮🇳' },
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'ta', name: 'தமிழ் (Tamil)', flag: '🇮🇳' },
    { code: 'te', name: 'తెలుగు (Telugu)', flag: '🇮🇳' },
    { code: 'bn', name: 'বাংলা (Bengali)', flag: '🇮🇳' },
    { code: 'mr', name: 'मराठी (Marathi)', flag: '🇮🇳' }
  ];

  const handleStartListening = () => {
    setIsListening(true);
    // Simulate voice recognition
    setTimeout(() => {
      setTranscript('मुझे फसल ऋण के बारे में जानकारी चाहिए');
      setResponse('हम फसल ऋण, व्यक्तिगत ऋण और शिक्षा ऋण प्रदान करते हैं। आप कौन सा ऋण चाहते हैं?');
      setIsListening(false);
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
          <span className="text-3xl mr-3">🎤</span>
          Voice Assistant
        </h2>
        <p className="text-gray-600">
          Speak in your language - I understand 10+ Indian languages!
        </p>
      </div>

      {/* Language Selector */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <h3 className="font-bold mb-4">🌍 Select Language</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {languages.map(lang => (
            <button
              key={lang.code}
              onClick={() => setLanguage(lang.code)}
              className={`p-3 rounded-lg border-2 transition-all ${
                language === lang.code
                  ? 'border-green-500 bg-green-50'
                  : 'border-gray-200 hover:border-green-300'
              }`}
            >
              <span className="text-2xl mr-2">{lang.flag}</span>
              <span className="text-sm font-medium">{lang.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Microphone */}
      <div className="bg-white rounded-xl shadow-md p-8 mb-6 text-center">
        <button
          onClick={handleStartListening}
          disabled={isListening}
          className={`w-32 h-32 rounded-full mx-auto transition-all transform hover:scale-105 ${
            isListening
              ? 'bg-red-500 animate-pulse'
              : 'bg-gradient-to-br from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600'
          }`}
        >
          <span className="text-6xl text-white">
            {isListening ? '🔴' : '🎤'}
          </span>
        </button>
        <p className="mt-4 text-gray-600 font-medium">
          {isListening ? 'Listening...' : 'Tap to speak'}
        </p>
      </div>

      {/* Transcript */}
      {transcript && (
        <div className="bg-blue-50 rounded-xl shadow-md p-6 mb-4">
          <h4 className="font-bold text-blue-800 mb-2">👤 You said:</h4>
          <p className="text-lg text-gray-800">{transcript}</p>
        </div>
      )}

      {/* Response */}
      {response && (
        <div className="bg-green-50 rounded-xl shadow-md p-6">
          <h4 className="font-bold text-green-800 mb-2">🤖 Assistant:</h4>
          <p className="text-lg text-gray-800 mb-4">{response}</p>
          <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-all">
            🔊 Play Audio Response
          </button>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow-md p-6 mt-6">
        <h3 className="font-bold mb-4">💬 Try These Commands:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            'मुझे ऋण चाहिए (I need a loan)',
            'मेरा खाता शेष क्या है? (What is my balance?)',
            'फसल का मूल्य क्या है? (What is crop price?)',
            'मुझे मदद चाहिए (I need help)'
          ].map((cmd, idx) => (
            <button
              key={idx}
              className="p-3 text-left bg-gray-50 hover:bg-green-50 border border-gray-200 hover:border-green-500 rounded-lg transition-all"
            >
              <span className="text-sm">{cmd}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default VoiceAssistant;
