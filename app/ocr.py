from fastapi import HTTPException
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  

def extract_text_from_image(image_io):
    """
    Extract text from a PIL image object passed in as a byte stream (like from a file).
    :param image_io: Byte stream of the image.
    :return: Extracted text from the image.
    """
    try:
        image = Image.open(image_io)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
