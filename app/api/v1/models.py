from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class BugReportDB(Base):
    __tablename__ = "bug_reports"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)