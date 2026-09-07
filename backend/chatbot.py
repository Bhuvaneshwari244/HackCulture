"""
Financial Literacy Chatbot
Interactive AI assistant for financial education
"""

import random
from datetime import datetime

class FinancialChatbot:
    def __init__(self):
        """Initialize financial literacy chatbot"""
        self.user_sessions = {}  # Track user progress
        self.modules = self._load_learning_modules()
        self.intents = self._load_intents()
        
    def _load_learning_modules(self):
        """Load financial literacy learning modules"""
        return {
            'savings': {
                'title': 'Smart Savings',
                'lessons': [
                    'Why save money?',
                    'Types of savings accounts',
                    'Setting savings goals',
                    'Emergency fund planning'
                ],
                'quiz': [
                    {
                        'question': 'What percentage of income should you save?',
                        'options': ['5%', '10-20%', '50%', '100%'],
                        'correct': 1,
                        'explanation': '10-20% is recommended for healthy financial growth'
                    }
                ]
            },
            'loans': {
                'title': 'Understanding Loans',
                'lessons': [
                    'What is a loan?',
                    'Types of loans',
                    'Interest rates explained',
                    'EMI calculation',
                    'Credit score importance'
                ],
                'quiz': [
                    {
                        'question': 'What does EMI stand for?',
                        'options': ['Easy Money Income', 'Equated Monthly Installment', 'Extra Money Interest', 'Electronic Money Index'],
                        'correct': 1,
                        'explanation': 'EMI is Equated Monthly Installment - the fixed amount you pay every month'
                    }
                ]
            },
            'insurance': {
                'title': 'Insurance Basics',
                'lessons': [
                    'Why insurance is important',
                    'Types of insurance',
                    'Crop insurance for farmers',
                    'Claim process'
                ],
                'quiz': [
                    {
                        'question': 'What is Pradhan Mantri Fasal Bima Yojana?',
                        'options': ['Health insurance', 'Crop insurance', 'Life insurance', 'Vehicle insurance'],
                        'correct': 1,
                        'explanation': 'PMFBY is a crop insurance scheme for farmers'
                    }
                ]
            },
            'digital_banking': {
                'title': 'Digital Banking',
                'lessons': [
                    'Online banking basics',
                    'Mobile banking apps',
                    'UPI and digital payments',
                    'Staying safe online'
                ],
                'quiz': [
                    {
                        'question': 'Should you share your bank OTP with anyone?',
                        'options': ['Yes, with bank staff', 'Yes, with family', 'No, never', 'Only on phone'],
                        'correct': 2,
                        'explanation': 'Never share OTP with anyone - not even bank staff!'
                    }
                ]
            },
            'government_schemes': {
                'title': 'Government Schemes',
                'lessons': [
                    'PM-KISAN scheme',
                    'Kisan Credit Card',
                    'MUDRA loans',
                    'Jan Dhan Yojana'
                ],
                'quiz': [
                    {
                        'question': 'How much does PM-KISAN provide annually?',
                        'options': ['₹2,000', '₹6,000', '₹10,000', '₹12,000'],
                        'correct': 1,
                        'explanation': 'PM-KISAN provides ₹6,000 per year in three installments'
                    }
                ]
            }
        }
    
    def _load_intents(self):
        """Load intent patterns and responses"""
        return {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'namaste', 'नमस्ते'],
                'responses': [
                    'Hello! I\'m here to help you learn about banking and finance. What would you like to know?',
                    'Namaste! Welcome to financial literacy learning. How can I help you today?',
                    'Hi there! Ready to learn about money management?'
                ]
            },
            'loan_help': {
                'patterns': ['loan', 'ऋण', 'credit', 'borrow', 'कर्ज'],
                'responses': [
                    'I can help you understand loans! Would you like to learn about:\n1. Types of loans\n2. How interest works\n3. Credit scores\n4. Loan application process',
                    'Loans can be helpful when used wisely. What specific aspect interests you?'
                ]
            },
            'savings_help': {
                'patterns': ['save', 'savings', 'बचत', 'deposit'],
                'responses': [
                    'Saving money is crucial for financial security. I can teach you about:\n1. Why saving matters\n2. Best savings accounts\n3. Setting goals\n4. Building emergency fund',
                    'Great question about savings! Let me help you understand how to save effectively.'
                ]
            },
            'insurance_help': {
                'patterns': ['insurance', 'बीमा', 'crop insurance', 'फसल बीमा'],
                'responses': [
                    'Insurance protects you from financial loss. Want to learn about:\n1. Crop insurance (PMFBY)\n2. Life insurance\n3. Health insurance\n4. How to claim',
                    'Insurance is essential for farmers. Let me explain the available options.'
                ]
            },
            'digital_banking': {
                'patterns': ['upi', 'digital', 'online banking', 'app', 'mobile banking'],
                'responses': [
                    'Digital banking makes life easier! I can explain:\n1. How to use UPI\n2. Mobile banking apps\n3. Safety tips\n4. Common problems',
                    'Let\'s learn about digital banking together. What would you like to know?'
                ]
            },
            'schemes': {
                'patterns': ['scheme', 'योजना', 'pm-kisan', 'government', 'सरकार'],
                'responses': [
                    'There are many government schemes for farmers:\n1. PM-KISAN\n2. Kisan Credit Card\n3. MUDRA loans\n4. Jan Dhan Yojana\n\nWhich one interests you?',
                    'Government schemes can help you grow. Let me explain the available benefits.'
                ]
            }
        }
    
    def process_message(self, data):
        """
        Process user message and return response
        
        Parameters:
        - user_id: User identifier
        - message: User message
        - language: Language code
        - session_id: Session identifier
        """
        user_id = data.get('user_id')
        message = data.get('message', '').lower()
        language = data.get('language', 'en')
        session_id = data.get('session_id')
        
        # Initialize session if needed
        if session_id not in self.user_sessions:
            self.user_sessions[session_id] = {
                'user_id': user_id,
                'completed_modules': [],
                'current_module': None,
                'points': 0,
                'streak': 0,
                'last_interaction': None
            }
        
        session = self.user_sessions[session_id]
        session['last_interaction'] = datetime.now()
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Check for specific commands
        if 'quiz' in message or 'test' in message:
            return self._start_quiz(session)
        
        if 'progress' in message or 'score' in message:
            return self._get_progress(session)
        
        if 'module' in message or 'course' in message:
            return self._list_modules()
        
        # Handle based on intent
        if intent:
            response_text = random.choice(self.intents[intent]['responses'])
        else:
            # Default response with suggestions
            response_text = (
                "I'm here to help you learn about banking and finance. "
                "You can ask me about:\n"
                "• Loans and credit\n"
                "• Savings and investments\n"
                "• Insurance\n"
                "• Digital banking\n"
                "• Government schemes\n\n"
                "Or type 'quiz' to test your knowledge!"
            )
        
        return {
            'success': True,
            'response': response_text,
            'session_id': session_id,
            'user_progress': {
                'points': session['points'],
                'completed_modules': len(session['completed_modules']),
                'streak': session['streak']
            },
            'suggestions': self._get_suggestions(intent),
            'interactive_elements': self._get_interactive_elements(intent)
        }
    
    def _detect_intent(self, message):
        """Detect user intent from message"""
        for intent, data in self.intents.items():
            for pattern in data['patterns']:
                if pattern in message:
                    return intent
        return None
    
    def _start_quiz(self, session):
        """Start a quiz for the user"""
        # Select a random module
        module_name = random.choice(list(self.modules.keys()))
        module = self.modules[module_name]
        
        if module['quiz']:
            question_data = random.choice(module['quiz'])
            
            return {
                'success': True,
                'response': f"📝 Quiz Time: {module['title']}\n\n{question_data['question']}",
                'quiz_data': {
                    'question': question_data['question'],
                    'options': question_data['options'],
                    'module': module_name
                },
                'interactive': True
            }
        
        return {
            'success': False,
            'response': 'No quiz available right now. Try learning a module first!'
        }
    
    def _get_progress(self, session):
        """Get user progress"""
        total_modules = len(self.modules)
        completed = len(session['completed_modules'])
        progress_percent = (completed / total_modules * 100) if total_modules > 0 else 0
        
        response = f"""
📊 Your Learning Progress

✅ Completed Modules: {completed}/{total_modules}
⭐ Points Earned: {session['points']}
🔥 Current Streak: {session['streak']} days
📈 Progress: {progress_percent:.0f}%

Keep learning to earn more points! 🎯
"""
        
        return {
            'success': True,
            'response': response.strip(),
            'progress_data': {
                'completed_modules': completed,
                'total_modules': total_modules,
                'points': session['points'],
                'streak': session['streak'],
                'progress_percent': progress_percent
            }
        }
    
    def _list_modules(self):
        """List all available learning modules"""
        response = "📚 Available Learning Modules:\n\n"
        
        for i, (key, module) in enumerate(self.modules.items(), 1):
            response += f"{i}. {module['title']}\n"
            response += f"   Lessons: {len(module['lessons'])}\n\n"
        
        response += "Reply with a module name to start learning!"
        
        return {
            'success': True,
            'response': response,
            'modules': list(self.modules.keys())
        }
    
    def _get_suggestions(self, intent):
        """Get contextual suggestions"""
        suggestions = {
            'greeting': ['Learn about loans', 'Savings tips', 'Take a quiz'],
            'loan_help': ['Calculate EMI', 'Check credit score', 'Loan types'],
            'savings_help': ['Savings calculator', 'Best accounts', 'Goal setting'],
            'insurance_help': ['Crop insurance', 'Claim process', 'Premium calculator'],
            'digital_banking': ['UPI guide', 'Safety tips', 'App tutorial'],
            'schemes': ['PM-KISAN details', 'KCC benefits', 'Apply online']
        }
        
        return suggestions.get(intent, ['Take quiz', 'View modules', 'Check progress'])
    
    def _get_interactive_elements(self, intent):
        """Get interactive elements like buttons"""
        if intent == 'loan_help':
            return {
                'type': 'buttons',
                'buttons': [
                    {'text': '📖 Learn About Loans', 'action': 'module:loans'},
                    {'text': '🧮 EMI Calculator', 'action': 'calculator:emi'},
                    {'text': '📊 Credit Score', 'action': 'check:credit_score'}
                ]
            }
        
        return None


# Example usage
if __name__ == '__main__':
    chatbot = FinancialChatbot()
    
    print("Financial Literacy Chatbot Demo")
    print("=" * 70)
    
    # Simulate conversation
    session_id = 'test_session_001'
    
    conversations = [
        "Hello!",
        "I want to learn about loans",
        "quiz",
        "progress"
    ]
    
    for user_message in conversations:
        print(f"\n👤 User: {user_message}")
        
        result = chatbot.process_message({
            'user_id': 'user_123',
            'message': user_message,
            'language': 'en',
            'session_id': session_id
        })
        
        print(f"🤖 Bot: {result['response']}")
        
        if result.get('suggestions'):
            print(f"💡 Suggestions: {', '.join(result['suggestions'])}")
