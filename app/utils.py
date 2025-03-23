import whisper
from io import BytesIO
from pydub import AudioSegment
import re
import tempfile
import spacy
from langdetect import detect


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
    # print(f"Detected language: {result['language']}")
    # print(f"Transcribed text: {result['text']}") 
    return result['text']

