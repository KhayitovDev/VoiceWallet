from fastapi import APIRouter, HTTPException, UploadFile, File
from io import BytesIO
from fastapi import Depends
from sqlalchemy.orm import Session
import uuid
from app.utils import extract_spending_info, transcribe_audio
from database.crud import add_expense
from database.database import get_db
from database.schemas import AudioProcessingResponse

router = APIRouter()

@router.post('/process-audio')
async def process_audio(user_id: uuid.UUID, audio: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        audio_bytes = await audio.read()
        audio_io = BytesIO(audio_bytes)
        
        transcribed_text = transcribe_audio(audio_io) 
        expenses_data = extract_spending_info(transcribed_text)
        
        add_expense(user_id=user_id, original_text=transcribed_text, expenses=expenses_data, db=db)  
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))