import React, { useState, useRef, useEffect } from 'react';

function Chatbot({ user }) {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: 'नमस्ते! मैं आपकी वित्तीय शिक्षा सहायक हूं। मैं आपकी कैसे मदद कर सकती हूं?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const quickReplies = [
    '🏦 Tell me about loans',
    '💰 How to save money?',
    '📱 Digital banking help',
    '🌾 Crop insurance info'
  ];

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      type: 'user',
      text: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // Simulate bot response
    setTimeout(() => {
      const botResponse = getBotResponse(input);
      setMessages(prev => [...prev, botResponse]);
      setLoading(false);
    }, 1000);
  };

  const getBotResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    
    let responseText = '';
    if (lowerInput.includes('loan') || lowerInput.includes('ऋण')) {
      responseText = 'I can help you understand loans! We offer:\n\n1. Crop Loans - For farming needs\n2. Personal Loans - For household needs\n3. Education Loans - For your children\n\nWhich one interests you?';
    } else if (lowerInput.includes('save') || lowerInput.includes('बचत')) {
      responseText = 'Saving money is important! Here are tips:\n\n✓ Save 10-20% of your income\n✓ Keep emergency fund\n✓ Use savings account\n✓ Set financial goals\n\nWould you like to learn more?';
    } else {
      responseText = 'I can help you with:\n• Loans and credit\n• Savings tips\n• Insurance information\n• Digital banking\n• Government schemes\n\nWhat would you like to know?';
    }

    return {
      type: 'bot',
      text: responseText,
      timestamp: new Date()
    };
  };

  const handleQuickReply = (reply) => {
    setInput(reply.replace(/[^\w\s]/gi, ''));
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-500 to-blue-500 p-6 text-white">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center text-2xl mr-4">
              🤖
            </div>
            <div>
              <h2 className="text-xl font-bold">Financial Literacy Assistant</h2>
              <p className="text-sm text-green-100">Always here to help you learn</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="h-96 overflow-y-auto p-6 bg-gray-50">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`mb-4 flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs md:max-w-md px-4 py-3 rounded-2xl ${
                  message.type === 'user'
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : 'bg-white text-gray-800 rounded-bl-none shadow'
                }`}
              >
                <p className="whitespace-pre-line">{message.text}</p>
                <p className={`text-xs mt-1 ${message.type === 'user' ? 'text-blue-100' : 'text-gray-400'}`}>
                  {message.timestamp.toLocaleTimeString('en-US', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </p>
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="bg-white px-4 py-3 rounded-2xl rounded-bl-none shadow">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Replies */}
        <div className="px-6 py-3 bg-white border-t border-gray-200">
          <div className="flex gap-2 overflow-x-auto">
            {quickReplies.map((reply, index) => (
              <button
                key={index}
                onClick={() => handleQuickReply(reply)}
                className="px-4 py-2 bg-gray-100 hover:bg-green-100 text-sm rounded-full whitespace-nowrap transition-all"
              >
                {reply}
              </button>
            ))}
          </div>
        </div>

        {/* Input */}
        <div className="p-4 bg-white border-t border-gray-200">
          <div className="flex space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your message..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="px-6 py-3 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-full hover:from-green-600 hover:to-blue-600 transition-all disabled:opacity-50 font-medium"
            >
              Send 📤
            </button>
          </div>
        </div>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <InfoCard
          icon="📚"
          title="Learning Modules"
          description="5 completed / 10 total"
          color="blue"
        />
        <InfoCard
          icon="⭐"
          title="Points Earned"
          description="450 points"
          color="yellow"
        />
        <InfoCard
          icon="🔥"
          title="Current Streak"
          description="7 days"
          color="orange"
        />
      </div>
    </div>
  );
}

function InfoCard({ icon, title, description, color }) {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    yellow: 'from-yellow-500 to-yellow-600',
    orange: 'from-orange-500 to-orange-600'
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color]} rounded-xl shadow-md p-4 text-white`}>
      <div className="text-3xl mb-2">{icon}</div>
      <h3 className="font-bold text-sm">{title}</h3>
      <p className="text-sm text-white/80">{description}</p>
    </div>
  );
}

export default Chatbot;
