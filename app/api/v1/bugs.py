from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.api.v1.db import SessionLocal
from app.api.v1.models import BugReportDB
from pydantic import BaseModel

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI router
router = APIRouter()

# Pydantic model for incoming bug report
class BugReport(BaseModel):
    title: str
    description: str
    severity: str  # Added this field to match the DB model

# Endpoint to receive and save bug reports
@router.post("/report-bug")
def report_bug(report: BugReport, db: Session = Depends(get_db)):
    bug_entry = BugReportDB(
        title=report.title,
        description=report.description,
        severity=report.severity
    )
    db.add(bug_entry)
    db.commit()
    db.refresh(bug_entry)
    return {
        "id": bug_entry.id,
        "title": bug_entry.title,
        "description": bug_entry.description,
        "status": "received"
    }