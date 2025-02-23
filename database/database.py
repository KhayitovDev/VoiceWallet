from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config


DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
Base = declarative_base()

class DBContext:
    def __init__(self) -> None:
        self.db = SessionLocal()
    
    def __enter__(self):
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        
def get_db():
    with DBContext() as db:
        yield db