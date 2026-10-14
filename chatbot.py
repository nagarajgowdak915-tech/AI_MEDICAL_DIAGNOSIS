
def get_chatbot_response(message, language):
    text = message.lower().strip()

    responses = {
        "English": {
            "greeting": "Hello! I can help with basic diabetes education. What would you like to know?",
            "diabetes": "Diabetes is a condition in which blood glucose levels become too high. A healthcare professional can assess and diagnose it.",
            "symptoms": "Possible symptoms include increased thirst, frequent urination, tiredness, and blurred vision. Some people have no symptoms. Consult a healthcare professional for assessment.",
            "doctor": "I cannot diagnose illness or recommend treatment. Please consult a qualified healthcare professional for personal medical advice.",
            "default": "I can answer basic questions about diabetes, its symptoms, and when to seek medical advice."
        },
        "Kannada": {
            "greeting": "ನಮಸ್ಕಾರ! ಮಧುಮೇಹದ ಬಗ್ಗೆ ಸಾಮಾನ್ಯ ಮಾಹಿತಿಯನ್ನು ನೀಡಬಲ್ಲೆ. ನಿಮಗೆ ಏನು ತಿಳಿಯಬೇಕು?",
            "diabetes": "ಮಧುಮೇಹವು ರಕ್ತದಲ್ಲಿನ ಗ್ಲೂಕೋಸ್ ಪ್ರಮಾಣ ಹೆಚ್ಚಾಗುವ ಆರೋಗ್ಯ ಸ್ಥಿತಿ. ಸರಿಯಾದ ಪತ್ತೆಗಾಗಿ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "symptoms": "ಹೆಚ್ಚಿದ ಬಾಯಾರಿಕೆ, ಪದೇಪದೇ ಮೂತ್ರ ವಿಸರ್ಜನೆ, ದಣಿವು ಮತ್ತು ದೃಷ್ಟಿ ಮಸುಕಾಗುವುದು ಕೆಲವು ಲಕ್ಷಣಗಳು. ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "doctor": "ನಾನು ರೋಗ ಪತ್ತೆ ಅಥವಾ ಚಿಕಿತ್ಸೆಯನ್ನು ನೀಡಲು ಸಾಧ್ಯವಿಲ್ಲ. ವೈಯಕ್ತಿಕ ವೈದ್ಯಕೀಯ ಸಲಹೆಗಾಗಿ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "default": "ಮಧುಮೇಹ, ಅದರ ಲಕ್ಷಣಗಳು ಮತ್ತು ವೈದ್ಯಕೀಯ ಸಲಹೆ ಯಾವಾಗ ಪಡೆಯಬೇಕು ಎಂಬುದರ ಬಗ್ಗೆ ಕೇಳಿ."
        },
        "Hindi": {
            "greeting": "नमस्ते! मैं मधुमेह के बारे में सामान्य जानकारी दे सकता हूँ। आप क्या जानना चाहते हैं?",
            "diabetes": "मधुमेह एक ऐसी स्थिति है जिसमें रक्त में ग्लूकोज़ का स्तर बढ़ जाता है। सही जाँच के लिए डॉक्टर से संपर्क करें।",
            "symptoms": "अधिक प्यास लगना, बार-बार पेशाब आना, थकान और धुंधला दिखाई देना कुछ लक्षण हैं। डॉक्टर से सलाह लें।",
            "doctor": "मैं बीमारी का निदान या उपचार नहीं कर सकता। व्यक्तिगत चिकित्सा सलाह के लिए डॉक्टर से संपर्क करें।",
            "default": "आप मधुमेह, उसके लक्षणों और डॉक्टर से कब मिलना चाहिए, इसके बारे में पूछ सकते हैं।"
        },
        "Tamil": {
            "greeting": "வணக்கம்! நீரிழிவு பற்றி பொதுவான தகவல்களை வழங்க முடியும். என்ன தெரிந்துகொள்ள விரும்புகிறீர்கள்?",
            "diabetes": "நீரிழிவு என்பது இரத்தத்தில் குளுக்கோஸ் அளவு அதிகரிக்கும் ஒரு நிலை. சரியான பரிசோதனைக்கு மருத்துவரை அணுகவும்.",
            "symptoms": "அதிக தாகம், அடிக்கடி சிறுநீர் கழித்தல், சோர்வு, மங்கலான பார்வை ஆகியவை சில அறிகுறிகள். மருத்துவரை அணுகவும்.",
            "doctor": "நான் நோயைக் கண்டறியவோ சிகிச்சை வழங்கவோ முடியாது. மருத்துவ ஆலோசனைக்கு மருத்துவரை அணுகவும்.",
            "default": "நீரிழிவு, அதன் அறிகுறிகள் மற்றும் மருத்துவரை எப்போது அணுக வேண்டும் என்று கேட்கலாம்."
        },
        "Telugu": {
            "greeting": "నమస్కారం! మధుమేహం గురించి సాధారణ సమాచారాన్ని అందించగలను. మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?",
            "diabetes": "మధుమేహం అనేది రక్తంలో గ్లూకోజ్ స్థాయి పెరిగే పరిస్థితి. సరైన నిర్ధారణ కోసం వైద్యుడిని సంప్రదించండి.",
            "symptoms": "అధిక దాహం, తరచుగా మూత్ర విసర్జన, అలసట, చూపు మసకబారడం కొన్ని లక్షణాలు. వైద్యుడిని సంప్రదించండి.",
            "doctor": "నేను వ్యాధిని నిర్ధారించలేను లేదా చికిత్స సూచించలేను. వైద్య సలహా కోసం వైద్యుడిని సంప్రదించండి.",
            "default": "మధుమేహం, దాని లక్షణాలు, వైద్యుడిని ఎప్పుడు సంప్రదించాలో అడగవచ్చు."
        }
    }

    lang = language if language in responses else "English"
    r = responses[lang]

    if any(word in text for word in ["hello", "hi", "hey", "ನಮಸ್ಕಾರ", "नमस्ते", "வணக்கம்", "నమస్కారం"]):
        return r["greeting"]

    if any(word in text for word in ["symptom", "লक्षण", "ಲಕ್ಷಣ", "அறிகுறி", "లక్షణ"]):
        return r["symptoms"]

    if any(word in text for word in ["doctor", "treatment", "medicine", "ವೈದ್ಯ", "डॉक्टर", "மருத்துவர்", "వైద్యుడు"]):
        return r["doctor"]

    if any(word in text for word in ["diabetes", "diabetic", "ಮಧುಮೇಹ", "मधुमेह", "நீரிழிவு", "మధుమేహం"]):
        return r["diabetes"]

    return r["default"]
