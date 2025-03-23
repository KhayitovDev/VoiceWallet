from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from database.database import Base
from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, object_session
from uuid import uuid4

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, unique=True)
    currency = Column(String, default="UZS")
    hashed_password = Column(String)
    
    @validates('first_name', 'last_name')
    def set_username(self, key, value):
        """Automatically set the username as first_name-last_name"""
        if self.first_name and self.last_name:
            self.username = f"{self.first_name.lower()}-{self.last_name.lower()}"
        return value
    
    def _generate_unique_username(self, base_username: str):
        """Generate a unique username by checking if it exists in the database."""
        session: Session = object_session(self) 
        counter = 1
        username = base_username

        while session.query(User).filter(User.username == username).first():
            username = f"{base_username}-{counter}"
            counter += 1

        return username

    
class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    voice_content = Column(Text, nullable=True)
    ocr_content = Column(Text, nullable=True)
    expense_category = Column(String, nullable=True)
    expense_name = Column(String, nullable=True)
    expense_amount = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    