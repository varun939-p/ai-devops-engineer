from fastapi import APIRouter
from sqlalchemy import text
from app.models.db import engine

router = APIRouter()

@router.get("/health/db")
def db_health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
