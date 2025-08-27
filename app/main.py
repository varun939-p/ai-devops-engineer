from fastapi import FastAPI
from app.api.v1.logs import router as logs_router
from app.db.session import engine
from app.db.base_class import Base
from app.models.logs import Log

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include router
app.include_router(logs_router, prefix="/api/v1")
