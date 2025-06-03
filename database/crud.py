from typing import Any, Dict, List, Optional
from fastapi import Depends
from sqlalchemy import asc, desc, text
from sqlalchemy.orm import Session
from database.bcrypt import hash_password
from database.models import User, Expenses, Category
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
        amount = expense.get('amount')
        category = expense.get('category')
        
        new_expense = Expenses(
            user_id = user_id,
            voice_content = original_text,
            ocr_content = None,
            expense_category = category,
            expense_name = item,
            expense_amount = amount,
            insertion_type = 'VOICE'
        )
        
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        
def add_expense_by_image(user_id: uuid.UUID, extracted_content: List[Dict[str, Any]], expenses: List[Dict[str, Any]], db: Session = Depends(get_db)):
    for expense in expenses:
        item = expense.get('item')
        amount = expense.get('amount')
        category = expense.get('category')

        if item and category and amount:
            # Convert comma to dot for decimal point
            if isinstance(amount, str):
                amount = amount.replace(',', '.')

            # Convert to Decimal to ensure proper numeric type
            from decimal import Decimal, InvalidOperation
            try:
                amount_decimal = Decimal(amount)
            except (InvalidOperation, TypeError):
                # Handle invalid amount format gracefully, e.g. skip or log error
                continue

            new_expense = Expenses(
                user_id=user_id,
                voice_content=None,
                ocr_content=extracted_content,
                expense_category=category,
                expense_name=item,
                expense_amount=amount_decimal,
                insertion_type='OCR'
            )
            
            db.add(new_expense)
            db.commit()
            db.refresh(new_expense)

        
def add_expense_manual(user_id: uuid.UUID, description: str, amount: str, category: str, db: Session = Depends(get_db)):
    
    new_expense = Expenses(
        user_id = user_id,
        voice_content = None,
        ocr_content = None,
        expense_category = category,
        expense_name = description,
        expense_amount = amount,
        insertion_type = 'Manual'
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

def get_unique_expense_categories(user_id: uuid.UUID, db: Session):
    auto_generated_categories = (
        db.query(Expenses.expense_category)
        .filter(Expenses.user_id == user_id)
        .distinct()
        .all()
    )
    
    manual_added_categories = (
        db.query(Category.name)  # Or whatever column holds category name
        .filter(Category.user_id == user_id)
        .distinct()
        .all()
    )

    # Unpack from list of tuples into plain lists
    auto_generated_categories = [category[0] for category in auto_generated_categories]
    manual_added_categories = [category[0] for category in manual_added_categories]
    
    return auto_generated_categories + manual_added_categories

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
    
def add_new_category(user_id: uuid.UUID, category_name: str, db: Session):
    
    category =  db.query(Category.name).filter(Category.user_id == user_id).count()
    if category > 0:
        return {"message": "Category has already been added"}
    new_category = Category(
        user_id = user_id,
        name = category_name
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
def get_current_month_expense_amount(user_id: uuid.UUID, start_date: str, end_date: str, db: Session):

    query = text("""
                 
        SELECT SUM(expense_amount) AS total_amount
        FROM expenses
        WHERE user_id = :user_id
          AND created_at >= :start_date
          AND created_at < :end_date
    """)

    result = db.execute(query, {
        "user_id": user_id,
        "start_date": start_date,
        "end_date": end_date
    }).scalar()
    
    return result or 0  