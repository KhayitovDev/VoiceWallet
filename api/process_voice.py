from fastapi import APIRouter, HTTPException, UploadFile, File
from io import BytesIO

from app.utils import extract_spending_info, transcribe_audio
from database.schemas import AudioProcessingResponse

router = APIRouter()

@router.post('/process-audio')
async def process_audio(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        audio_io = BytesIO(audio_bytes)
        
        transcribed_text = transcribe_audio(audio_io)
        amount = extract_spending_info(transcribed_text)
        
        print(amount)
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))