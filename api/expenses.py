from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from uuid import UUID

from database.database import get_db
from database.crud import get_expenses_list

router = APIRouter()

@router.get('/expenses-list')
def get_user_expenses(user_id: UUID, db: Session=Depends(get_db)):
    return get_expenses_list(user_id=user_id, db=db)