from fastapi import FastAPI
from app.api.v1.bugs import router as bugs_router
from app.api.v1.models import Base
from app.api.v1.db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(bugs_router, prefix="/api/v1")
