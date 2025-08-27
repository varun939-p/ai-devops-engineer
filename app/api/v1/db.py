from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()