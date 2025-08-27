from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import SessionLocal
from app.models.logs import Log

router = APIRouter()

class LogEntry(BaseModel):
    source: str
    message: str
    level: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ingest-logs")
def ingest_logs(log: LogEntry, db: Session = Depends(get_db)):
    try:
        log_record = Log(
            source=log.source,
            message=log.message,
            level=log.level,
            timestamp=datetime.utcnow()
        )
        db.add(log_record)
        db.commit()
        db.refresh(log_record)
        return {
            "status": "saved",
            "id": log_record.id,
            "timestamp": log_record.timestamp.isoformat(),
            "log": log
        }
    except Exception as e:
        print("?? ERROR in ingest_logs:", e)
        raise

@router.get("/view-logs")
def view_logs(source: str = None, level: str = None, limit: int = 50, db: Session = Depends(get_db)):
    """
    Fetch logs with optional filters and limit
    """
    try:
        query = db.query(Log)

        if source:
            query = query.filter(Log.source == source)
        if level:
            query = query.filter(Log.level == level)

        logs = query.order_by(Log.timestamp.desc()).limit(limit).all()

        return [
            {
                "id": log.id,
                "source": log.source,
                "message": log.message,
                "level": log.level,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]
    except Exception as e:
        print("?? ERROR in view_logs:", e)
        raise

from datetime import datetime

@router.get("/view-logs")
def view_logs(
    source: str = None,
    level: str = None,
    limit: int = 50,
    start_time: str = None,  # ISO format: YYYY-MM-DDTHH:MM:SS
    end_time: str = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Log)

        if source:
            query = query.filter(Log.source == source)
        if level:
            query = query.filter(Log.level == level)
        if start_time:
            query = query.filter(Log.timestamp >= datetime.fromisoformat(start_time))
        if end_time:
            query = query.filter(Log.timestamp <= datetime.fromisoformat(end_time))

        logs = query.order_by(Log.timestamp.desc()).limit(limit).all()

        return [
            {
                "id": log.id,
                "source": log.source,
                "message": log.message,
                "level": log.level,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]
    except Exception as e:
        print("?? ERROR in view_logs:", e)
        raise

@router.get("/view-logs-extended")
def view_logs_extended(
    source: str = None,
    level: str = None,
    message_contains: str = None,
    limit: int = 50,
    start_time: str = None,
    end_time: str = None,
    sort_order: str = "desc",
    count_only: bool = False,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Log)
        from datetime import datetime

        if source:
            query = query.filter(Log.source == source)
        if level:
            query = query.filter(Log.level == level)
        if message_contains:
            query = query.filter(func.lower(Log.message).contains(message_contains.lower()))
        if start_time:
            query = query.filter(Log.timestamp >= datetime.fromisoformat(start_time))
        if end_time:
            query = query.filter(Log.timestamp <= datetime.fromisoformat(end_time))

        query = query.order_by(Log.timestamp.asc() if sort_order == "asc" else Log.timestamp.desc())
        if count_only:
            return {"count": query.count()}

        logs = query.limit(limit).all()
        return [
            {
                "id": log.id,
                "source": log.source,
                "message": log.message,
                "level": log.level,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]
    except Exception as e:
        print("?? ERROR in view_logs_extended:", e)
        raise

from sqlalchemy import func
