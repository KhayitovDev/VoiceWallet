from typing import Optional
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from uuid import UUID

from database.database import get_db
from database.crud import (
    get_expenses_list, 
    get_unique_expense_categories,
    expense_update,
    expense_delete
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
async def get_list_of_categories(db: Session = Depends(get_db)):
     return get_unique_expense_categories(db=db)
 
@router.put('/update-expense')
async def update_existing_expense(expense_id: UUID, updated_expense: ExpenseUpdate, db: Session = Depends(get_db)):
    updated_data = updated_expense.model_dump()
    updated_expense = expense_update(expense_id=expense_id, updated_data=updated_data, db=db)
    return updated_expense

@router.delete('/delete-expense')
async def delete_existing_expense(expense_id: UUID, db: Session = Depends(get_db)):
    return expense_delete(expense_id=expense_id, db=db)