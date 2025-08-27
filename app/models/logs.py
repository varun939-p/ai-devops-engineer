from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base_class import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    message = Column(String)
    level = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
