import whisper
import re

# Load the Whisper model
model = whisper.load_model('base')

def transcribe_audio(file_path: str):
    # Corrected the argument passing
    result = model.transcribe(file_path)
    return result['text']

def extract_amount(text: str) -> float:
    """Extract the amount of money from transcribed text"""
    match = re.search(r"(\d+(?:\.\d+)?)\s*(dollars?|[\$])", text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return 0.0

# Example of usage:
audio_file = "luvvoice.com-20250223-erBuVl.mp3"
transcribed_text = transcribe_audio(audio_file)  # Uzbek language
print("Transcription: ", transcribed_text)

amount = extract_amount(transcribed_text)
print("Extracted Amount: ", amount)
