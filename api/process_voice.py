from fastapi import APIRouter, HTTPException, UploadFile, File
from io import BytesIO
from fastapi import Depends
from sqlalchemy.orm import Session
import uuid
from app.ocr import extract_text_from_image
from app.test import generate_content_async
from app.utils import transcribe_audio
from database.crud import add_expense_by_voice, add_expense_by_image
from database.database import get_db
from database.schemas import AudioProcessingResponse
import traceback
router = APIRouter()

@router.post('/process-audio')
async def process_audio(user_id: uuid.UUID, audio: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        audio_bytes = await audio.read()
        audio_io = BytesIO(audio_bytes)
        
        transcribed_text = transcribe_audio(audio_io) 
        print(f"ORIGINAL TEXT: {transcribed_text}")
        #expenses_data = await generate_content_async(transcribed_text)
        
        #print(f"EXPENSES: {expenses_data}")
        #add_expense_by_voice(user_id=user_id, original_text=transcribed_text, expenses=expenses_data, db=db)  
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    

@router.post('/process-image')
async def process_image(user_id: uuid.UUID, image: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
     
        image_bytes = await image.read()
        image_io = BytesIO(image_bytes)
        extracted_text = extract_text_from_image(image_io)
        print(f"EXTRACTED TEXT: {extracted_text}")

        if extracted_text:
            expenses_data = await generate_content_async(extracted_text)
            add_expense_by_image(user_id=user_id, extracted_content=extracted_text, expenses=expenses_data, db=db)
            print(f"EXPENSES: {expenses_data}")
            return {"extracted_text": extracted_text}
        

    except Exception as e:
        traceback.print_exc()       
        raise HTTPException(status_code=500, detail=str(e))