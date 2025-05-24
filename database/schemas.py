from typing import Any, List, Optional
from pydantic import BaseModel, field_validator

from sqlalchemy import Text

from uuid import UUID
from enum import Enum

class UserLogin(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str

class UserBase(BaseModel):
    username: str
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    
class UserCreate(UserBase):
    username: str
    hashed_password: str
    email: str
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # currency: Optional[str] = None
      
class UserResponse(UserBase):
    id: UUID
    username: str
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
   
    
class AudioProcessingResponse(BaseModel):
    transcription: str
    amount: float    
    

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    updated_at: Optional[Any] = None 

    class Config:
        from_attributes = True  

    