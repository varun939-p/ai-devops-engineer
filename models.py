from pydantic import BaseModel

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
