from sqlalchemy.orm import Session
from database.bcrypt import hash_password
from database.models import User
from database.schemas import UserBase, UserCreate, UserLogin, UserResponse


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