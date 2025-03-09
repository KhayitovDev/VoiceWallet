import whisper
from io import BytesIO
from pydub import AudioSegment
import re
import tempfile
import spacy
from langdetect import detect

from app.categories import CATEGORIES 


nlp = spacy.load("xx_ent_wiki_sm")
model = whisper.load_model('base')

def transcribe_audio(file: BytesIO) -> str:
    audio = AudioSegment.from_file(file)
    audio = audio.set_channels(1).set_frame_rate(16000)
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)  

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        tmp_file.write(buffer.read()) 
        tmp_file_path = tmp_file.name 

 
    result = model.transcribe(tmp_file_path) 
    print(f"Detected language: {result['language']}")
    
    return result['text']


def detect_language(text: str) -> str:
    """Detect the language of the text."""
    return detect(text)

def extract_spending_info(text):
    language = detect_language(text)
    print(f"COMING TEXT TO HERE: {text}")
    price_pattern = r"([€$₹¥])?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
    prices = re.findall(price_pattern, text)
    print(f"FOUND PRICES: {prices}")
    
    spending_details = []
    doc = nlp(text)
    
    for price in prices:
        currency_symbol, amount_str = price
        if not amount_str:
            continue

        amount = float(amount_str.replace(',', ''))
        if currency_symbol == '$':
            currency = 'USD'
        elif currency_symbol == '€':
            currency = 'EUR'
        elif currency_symbol == '₹':
            currency = 'INR'
        elif currency_symbol == '¥':
            currency = 'JPY'
        else:
            currency = 'Unknown'
        
        start_index = text.find(amount_str)
        text_after_price = text[start_index + len(amount_str):]
        
        item = None
        category_label = None
        

        for category, language_dict in CATEGORIES.items():
            for lang, keywords in language_dict.items():
                if lang == language:
                    for keyword in keywords:
                        if keyword.lower() in text_after_price.lower():
                            item = keyword
                            category_label = category
                            break
                if item:
                    break
            if item:
                break
        
        if not item:
            for token in doc[start_index:]:
                if token.pos_ == 'NOUN' and token.text.lower() not in [item.lower() for item in sum([list(cat.values()) for cat in CATEGORIES.values()], [])]:
                    item = token.text
                    category_label = 'general'
                    break
        
        if item:
            spending_details.append({
                'item': item,
                'amount': amount,
                'currency': currency,
                'category': category_label
            })
    
    return spending_details