from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()
class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)  
    level = Column(String, index=True)
    message = Column(String, index=True)
from sqlalchemy.orm import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
