
import json
from google import genai
from decouple import config


API_KEY = config("API_KEY")
client = genai.Client(api_key=API_KEY)

async def generate_content_async(text: str):
   
    content = f"""
    Extract the following information from the given text and return it as a JSON array:

    1. **Item**: The specific product or goods mentioned (e.g., Jacket, charger, bananas).
    2. **Category**: The general group or classification the item belongs to (e.g., clothing, electronics, food).
    3. **Amount**: The numerical value associated with each item or the total cost (e.g., 55, 15, 5).
    4. **Currency**: The type of currency used (e.g., USD, EUR, INR).

    Each item should be returned as an object in the JSON array with the structure:

    [
        {{
            "item": "<item_name>",
            "category": "<category>",
            "amount": "<amount>",
            "currency": "<currency>"
        }},
        
    ]

    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=content
    )

    cleaned_response = response.text.strip()  
    cleaned_response = cleaned_response.strip('```json').strip('```')  

    try:
        json_response = json.loads(cleaned_response)
        return json_response
    except json.JSONDecodeError:
        print("The response is not in valid JSON format:", cleaned_response)
    
    


  