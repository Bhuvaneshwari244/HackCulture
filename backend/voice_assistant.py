"""
Multilingual Voice Assistant for Rural Banking
Supports: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia
"""

import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import tempfile

class VoiceAssistant:
    def __init__(self):
        """Initialize voice assistant with multilingual support"""
        self.recognizer = sr.Recognizer()
        
        # Language code mapping
        self.language_map = {
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'or': 'Odia',
            'en': 'English'
        }
        
        # Common banking queries and responses in multiple languages
        self.responses = self._load_responses()
    
    def _load_responses(self):
        """Load predefined responses in multiple languages"""
        return {
            'greeting': {
                'hi': 'नमस्ते! मैं आपकी बैंकिंग सहायक हूं। मैं आपकी कैसे मदद कर सकती हूं?',
                'ta': 'வணக்கம்! நான் உங்கள் வங்கி உதவியாளர். நான் உங்களுக்கு எப்படி உதவ முடியும்?',
                'te': 'నమస్కారం! నేను మీ బ్యాంకింగ్ సహాయకుడిని. నేను మీకు ఎలా సహాయం చేయగలను?',
                'bn': 'নমস্কার! আমি আপনার ব্যাংকিং সহায়ক। আমি আপনাকে কীভাবে সাহায্য করতে পারি?',
                'mr': 'नमस्कार! मी तुमचा बँकिंग सहाय्यक आहे। मी तुम्हाला कशी मदत करू शकतो?',
                'gu': 'નમસ્તે! હું તમારો બેન્કિંગ સહાયક છું. હું તમને કેવી રીતે મદદ કરી શકું?',
                'kn': 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಬ್ಯಾಂಕಿಂಗ್ ಸಹಾಯಕ. ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?',
                'ml': 'നമസ്കാരം! ഞാൻ നിങ്ങളുടെ ബാങ്കിംഗ് അസിസ്റ്റന്റാണ്. ഞാൻ നിങ്ങളെ എങ്ങനെ സഹായിക്കും?',
                'pa': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਬੈਂਕਿੰਗ ਸਹਾਇਕ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?',
                'or': 'ନମସ୍କାର! ମୁଁ ଆପଣଙ୍କର ବ୍ୟାଂକିଂ ସହାୟକ। ମୁଁ ଆପଣଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରିବି?',
                'en': 'Hello! I am your banking assistant. How can I help you?'
            },
            'loan_info': {
                'hi': 'हम फसल ऋण, व्यक्तिगत ऋण और शिक्षा ऋण प्रदान करते हैं। आप कौन सा ऋण चाहते हैं?',
                'ta': 'நாங்கள் பயிர் கடன், தனிநபர் கடன் மற்றும் கல்வி கடன் வழங்குகிறோம். நீங்கள் எந்த கடனை விரும்புகிறீர்கள்?',
                'te': 'మేము పంట రుణాలు, వ్యక్తిగత రుణాలు మరియు విద్యా రుణాలను అందిస్తాము. మీకు ఏ రుణం కావాలి?',
                'en': 'We provide crop loans, personal loans, and education loans. Which loan do you need?'
            },
            'balance': {
                'hi': 'आपका खाता शेष जानने के लिए, मैं आपका खाता नंबर सत्यापित करूंगी।',
                'ta': 'உங்கள் கணக்கு இருப்பை அறிய, நான் உங்கள் கணக்கு எண்ணை சரிபார்க்கிறேன்.',
                'te': 'మీ ఖాతా బ్యాలెన్స్ తెలుసుకోవడానికి, నేను మీ ఖాతా నంబర్‌ను ధృవీకరిస్తాను.',
                'en': 'To check your account balance, I will verify your account number.'
            },
            'help': {
                'hi': 'मैं आपकी मदद कर सकती हूं: ऋण आवेदन, खाता शेष, भुगतान इतिहास, या वित्तीय सलाह के लिए।',
                'ta': 'நான் உங்களுக்கு உதவ முடியும்: கடன் விண்ணப்பம், கணக்கு இருப்பு, பணம் செலுத்தும் வரலாறு அல்லது நிதி ஆலோசனை.',
                'te': 'నేను మీకు సహాయం చేయగలను: రుణ దరఖాస్తు, ఖాతా బ్యాలెన్స్, చెల్లింపు చరిత్ర లేదా ఆర్థిక సలహా.',
                'en': 'I can help you with: loan application, account balance, payment history, or financial advice.'
            }
        }
    
    def process_audio(self, audio_file, language='hi'):
        """
        Process audio input and return text + audio response
        
        Args:
            audio_file: Audio file object
            language: Language code (hi, ta, te, etc.)
        
        Returns:
            dict with transcribed_text, response_text, and audio_url
        """
        try:
            # Save uploaded audio temporarily
            temp_audio_path = tempfile.mktemp(suffix='.wav')
            audio_file.save(temp_audio_path)
            
            # Convert speech to text
            transcribed_text = self._speech_to_text(temp_audio_path, language)
            
            # Process the query and get response
            response_text = self._get_response(transcribed_text, language)
            
            # Convert response to speech
            audio_url = self._text_to_speech(response_text, language)
            
            # Cleanup
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            
            return {
                'success': True,
                'transcribed_text': transcribed_text,
                'response_text': response_text,
                'audio_url': audio_url,
                'language': self.language_map.get(language, 'Unknown')
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _speech_to_text(self, audio_path, language):
        """Convert speech to text using speech recognition"""
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                # Use Google Speech Recognition with language support
                text = self.recognizer.recognize_google(audio_data, language=language)
                return text
        except sr.UnknownValueError:
            return "[Could not understand audio]"
        except sr.RequestError as e:
            return f"[Speech recognition error: {str(e)}]"
    
    def _get_response(self, query, language):
        """Get appropriate response based on query"""
        query_lower = query.lower()
        
        # Keyword matching for different intents
        if any(word in query_lower for word in ['loan', 'ऋण', 'கடன்', 'రుణం', 'लोन']):
            return self.responses['loan_info'].get(language, self.responses['loan_info']['en'])
        
        elif any(word in query_lower for word in ['balance', 'शेष', 'இருப்பு', 'బ్యాలెన్స్', 'બેલેન્સ']):
            return self.responses['balance'].get(language, self.responses['balance']['en'])
        
        elif any(word in query_lower for word in ['help', 'मदद', 'உதவி', 'సహాయం', 'मदत']):
            return self.responses['help'].get(language, self.responses['help']['en'])
        
        else:
            # Default greeting
            return self.responses['greeting'].get(language, self.responses['greeting']['en'])
    
    def _text_to_speech(self, text, language):
        """Convert text to speech and return audio file path"""
        try:
            # Generate unique filename
            filename = f"response_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
            filepath = os.path.join('static', 'audio', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Generate speech
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(filepath)
            
            return f"/static/audio/{filename}"
        
        except Exception as e:
            return None
    
    def text_to_speech_direct(self, text, language='hi'):
        """Direct text to speech conversion (useful for chatbot responses)"""
        return self._text_to_speech(text, language)


# Example usage and testing
if __name__ == '__main__':
    assistant = VoiceAssistant()
    
    print("Voice Assistant Test")
    print("=" * 50)
    print("\nSupported Languages:")
    for code, name in assistant.language_map.items():
        print(f"  {code}: {name}")
    
    print("\n\nSample Responses:")
    print("-" * 50)
    
    for intent, translations in assistant.responses.items():
        print(f"\n{intent.upper()}:")
        for lang in ['hi', 'ta', 'en']:
            if lang in translations:
                print(f"  {assistant.language_map[lang]}: {translations[lang]}")
    
    print("\n\nVoice Assistant ready for audio processing!")
