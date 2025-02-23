from fastapi import FastAPI, File, UploadFile
from app.utils import transcribe_audio, extract_amount
from app.categories import categorize_expense

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to VoiceWallet API"}



# Store expenses in-memory (you can replace this with a database later)
expenses = []

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    with open(f"temp_{file.filename}", "wb") as buffer:
        buffer.write(await file.read())

    # Transcribe audio to text
    transcribed_text = transcribe_audio(f"temp_{file.filename}")

    # Extract category
    category = await categorize_expense(transcribed_text)

    # Extract the amount from the text
    amount = extract_amount(transcribed_text)

    # Log the expense
    expense = {"amount": amount, "description": transcribed_text, "category": category}
    expenses.append(expense)

    return {"message": "Expense logged successfully", "expense": expense}
