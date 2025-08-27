from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class BugReport(BaseModel):
    title: str
    description: str
    severity: str

@router.post("/report-bug")
def report_bug(bug: BugReport):
    return {"message": "Bug report received", "bug": bug}
