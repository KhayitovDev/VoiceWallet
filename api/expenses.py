from typing import Optional
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from uuid import UUID

from database.database import get_db
from database.crud import (
    get_current_month_expense_amount,
    get_expenses_list, 
    get_unique_expense_categories,
    expense_update,
    expense_delete,
    add_expense_manual, 
    add_new_category
)
from database.schemas import ExpenseUpdate


router = APIRouter()

@router.get('/expenses-list')
async def get_user_expenses(
    user_id: UUID,
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = 'created_at',
    sort_order: Optional[str] = 'desc'
):
    return get_expenses_list(
        user_id=user_id,
        db=db,
        category=category,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
@router.get("/categories")
async def get_list_of_categories(user_id: UUID, db: Session = Depends(get_db)):
     return get_unique_expense_categories(user_id=user_id, db=db)
 
@router.put('/update-expense')
async def update_existing_expense(expense_id: UUID, updated_expense: ExpenseUpdate, db: Session = Depends(get_db)):
    updated_data = updated_expense.model_dump()
    updated_expense = expense_update(expense_id=expense_id, updated_data=updated_data, db=db)
    return updated_expense

@router.delete('/delete-expense')
async def delete_existing_expense(expense_id: UUID, db: Session = Depends(get_db)):
    return expense_delete(expense_id=expense_id, db=db)

@router.post('/add-expense-manual/')
async def add_expense_manually(user_id: UUID, item_name: str, amount: str, category: str, db: Session = Depends(get_db)):
    return add_expense_manual(user_id=user_id, description=item_name, amount=amount, category=category, db=db)

@router.post('/add-new-category/')
async def add_category_manually(user_id: UUID, category_name: str, db: Session = Depends(get_db)):
    return add_new_category(user_id=user_id, category_name=category_name, db=db)

@router.get('/expense-amount/')
async def get_expense_amount_within_range(user_id: UUID, start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    return get_current_month_expense_amount(user_id=user_id, start_date=start_date, end_date=end_date, db=db)
