

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User




from api import users

import json
from uuid import UUID

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
        "https://12d6-94-158-60-201.ngrok-free.app",
        "http://localhost:5173", 
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/static", StaticFiles(directory="static/"), name="static")

app.include_router(users.router, prefix="/api/users", tags=["users"])