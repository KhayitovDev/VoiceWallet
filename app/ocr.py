import easyocr
from fastapi import HTTPException
from io import BytesIO
from PIL import Image
import numpy as np

def extract_text_from_image(image_io):
    """
    Extract text from a PIL image object passed in as a byte stream (like from a file).
    :param image_io: Byte stream of the image.
    :return: Extracted text from the image.
    """
    try:
        # Correct language list for Cyrillic languages
        reader = easyocr.Reader(['en', 'ru', 'uk', 'be', 'bg', 'mn'])  # Correct list for Cyrillic languages

        # Open the image using PIL
        image = Image.open(image_io)

        # Convert PIL image to a format EasyOCR can read (numpy array)
        image_array = np.array(image)

        # Extract text using EasyOCR
        result = reader.readtext(image_array)

        # Join all extracted texts into a single string
        extracted_text = "\n".join([text[1] for text in result])

        return extracted_text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
