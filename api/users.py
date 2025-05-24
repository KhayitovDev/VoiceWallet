from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from decouple import config

from typing import List
from datetime import datetime, timedelta, timezone
from uuid import UUID

from database import crud, schemas, bcrypt
from database.database import get_db
from database.models import User
from database.utils import verify_password, create_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    crud.create_user(db, user)
    return {"message": "Your account has been created successfully!"}


@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session=Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/get_user_id/{username}")
def get_user_id(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if user:
        return {"user_id": user.id}
    else:
        return {"error": "User not found"}, 404
