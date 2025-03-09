from typing import Any, Dict, List
from fastapi import Depends
from sqlalchemy.orm import Session
from database.bcrypt import hash_password
from database.models import User, Expenses
from database.schemas import UserBase, UserCreate, UserLogin, UserResponse
import uuid
from database.database import get_db

def create_user(db: Session, user: UserCreate):
    user_hash_password = hash_password(user.hashed_password)
    
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=user_hash_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def add_expense(user_id: uuid.UUID,  original_text: str,  expenses: List[Dict[str, Any]], db: Session = Depends(get_db)):
    
    print(len(expenses))
    for expense in expenses:
        item = expense.get('item')
        print(f"ITEM: {item}")
        amount = expense.get('amount')
        print(f"AMOUNT: {amount}")
        category = expense.get('category')
        print(f"CATEGORY: {category}")
        
        new_expense = Expenses(
            user_id = user_id,
            voice_content = original_text,
            expense_category = category,
            expense_name = item,
            expense_amount = amount
        )
        
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)