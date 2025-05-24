

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User




from api import users, process_voice, expenses


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    
        "http://localhost",
        "http://localhost:8000",
        "https://12d6-94-158-60-201.ngrok-free.app",
        "http://localhost:5173", 
        "http://localhost:5174",
        "https://vermillion-kangaroo-33e132.netlify.app",
        "http://172.28.112.1:8001",
        "http://10.0.2.2:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/static", StaticFiles(directory="static/"), name="static")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(process_voice.router, prefix="/api/process-audio", tags=["audio-process"])
app.include_router(expenses.router, prefix="/api/expenses")