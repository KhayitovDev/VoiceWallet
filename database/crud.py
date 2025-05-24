from typing import Any, Dict, List, Optional
from fastapi import Depends
from sqlalchemy import asc, desc
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
        email=user.email,
        hashed_password=user_hash_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def add_expense_by_voice(user_id: uuid.UUID,  original_text: str,  expenses: List[Dict[str, Any]], db: Session = Depends(get_db)):
    
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
            ocr_content = None,
            expense_category = category,
            expense_name = item,
            expense_amount = amount
        )
        
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        
def add_expense_by_image(user_id: uuid.UUID,  extracted_content: List[Dict[str, Any]],  expenses: List[Dict[str, Any]], db: Session = Depends(get_db)):
    
    for expense in expenses:
        item = expense.get('item')
        print(f"ITEM: {item}")
        amount = expense.get('amount')
        print(f"AMOUNT: {amount}")
        category = expense.get('category')
        print(f"CATEGORY: {category}")
        if item and category and amount:
            new_expense = Expenses(
                user_id = user_id,
                voice_content = None,
                ocr_content = extracted_content,
                expense_category = category,
                expense_name = item,
                expense_amount = amount
            )
            
            db.add(new_expense)
            db.commit()
            db.refresh(new_expense)
        
def get_expenses_list(
    user_id: uuid.UUID,
    db: Session,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = 'created_at',
    sort_order: Optional[str] = 'desc'
):
    query = db.query(Expenses).filter(Expenses.user_id == user_id)

    if category:
        query = query.filter(Expenses.expense_category == category)

    if search:
        query = query.filter(
            (Expenses.voice_content.ilike(f'%{search}%')) |
            (Expenses.ocr_content.ilike(f'%{search}%')) |
            (Expenses.expense_name.ilike(f'%{search}%'))
        )

    if sort_order == 'asc':
        if sort_by in ['created_at', 'expense_amount', 'expense_name']:  
            query = query.order_by(asc(getattr(Expenses, sort_by)))
    else:
        if sort_by in ['created_at', 'expense_amount', 'expense_name']:  
            query = query.order_by(desc(getattr(Expenses, sort_by)))

    return query.all()

def get_unique_expense_categories(db: Session):
    categories = db.query(Expenses.expense_category).distinct().all()
    return [category[0] for category in categories]

def expense_delete(expense_id: uuid.UUID, db: Session):
    expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
    
    if expense:
        db.delete(expense)
        db.commit()
        return {"message": "Expense deleted successfully"}
    else:
        return {"message": "Expense not found"}
    
def expense_update(expense_id: uuid.UUID, updated_data: dict, db: Session):
    expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
    
    if expense:
        for key, value in updated_data.items():
            if key == "updated_at":
                pass 
            else:   
                if hasattr(expense, key):
                    setattr(expense, key, value)
                
        db.commit()
        return {"message": "Expense updated successfully"}
    else:
        return {"message": "Expense not found"}