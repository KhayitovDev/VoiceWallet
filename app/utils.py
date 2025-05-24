import os
import whisper
from io import BytesIO
from pydub import AudioSegment
import re
import tempfile
import spacy
from langdetect import detect


# Load Whisper model
model = whisper.load_model('base')

def transcribe_audio(file: BytesIO) -> str:
    # Load and preprocess the audio file
    try:
        audio = AudioSegment.from_file(file)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return "Error loading audio file"

    # Ensure the audio is mono and at the correct sample rate (16kHz)
    audio = audio.set_channels(1).set_frame_rate(16000)
    
    # Check if the audio length is zero or too short
    if len(audio) == 0:
        print("Audio file is empty or has no content.")
        return "Audio is empty"

    # Create a temporary WAV file for Whisper to process
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        tmp_file.write(buffer.read()) 
        tmp_file_path = tmp_file.name 

    # Debugging: Check the temporary file size
    if os.path.getsize(tmp_file_path) < 1000:  # less than 1KB
        print("Temporary file seems too small. Likely an issue with audio conversion.")
        return "Error: Audio conversion issue"

    # Transcribe using Whisper
    try:
        result = model.transcribe(tmp_file_path)
    except Exception as e:
        print(f"Error during transcription: {e}")
        return "Error during transcription"

    # Extract detected language and transcribed text
    detected_language = result.get('language', 'unknown')
    transcribed_text = result.get('text', '').strip()
    
    # Debugging: Check if transcription was successful
    if not transcribed_text:
        print(f"Whisper detected language: {detected_language}, but no text was transcribed.")
        return "No text transcribed"

    # Optionally, print the detected language and transcribed text
    print(f"Detected language: {detected_language}")
    print(f"Transcribed text: {transcribed_text}")
    
    return transcribed_text