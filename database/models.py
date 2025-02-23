from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid4)
    first_name =  Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String)
    
class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    expense_type = Column(String, nullable=True)
    voice_content = Column(Text, nullable=True)
    amount = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    