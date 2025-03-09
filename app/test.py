import spacy
import re

# Assuming the CATEGORIES dictionary is correctly defined as per your request.
from categories import CATEGORIES
from utils import detect_language
nlp = spacy.load('xx_ent_wiki_sm')

def extract_spending_info(text):
   
    language = detect_language(text=text)
    print(f"COMING TEXT TO HERE: {text}")
    
   
    price_pattern = r"([€$₹¥])?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
    prices = re.findall(price_pattern, text)

    
    spending_details = []
    doc = nlp(text)  
 
    price_positions = [m.start() for m in re.finditer(price_pattern, text)]
    
    for i, price in enumerate(prices):
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
        

        start_index = price_positions[i]
        end_index = price_positions[i + 1] if i + 1 < len(price_positions) else len(text)
        text_after_price = text[start_index:end_index]
        
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

# Example text to test
text = "13 $ per un caffè, 25 $ per una giacca e 10 $ per il caricabatteria."

result = extract_spending_info(text)
print(result)
