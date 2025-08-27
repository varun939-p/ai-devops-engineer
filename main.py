from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI-DevOps backend is live"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/db")
def health_db():
    try:
        # TODO: Replace with your real DB connectivity check
        return {"status": "ok", "db": "healthy"}
    except Exception as e:
        return {"status": "error", "db": str(e)}

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

@app.get("/api/logs")
def get_logs():
    # Placeholder response ? wire to DB later
    return JSONResponse(content={"logs": []})

if __name__ == "__main__":
    reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"
    print("[AI-DevOps] Import succeeded - launching FastAPI server...")
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=reload_flag)
from sqlalchemy.orm import Session
from database import SessionLocal, Log

@app.get("/api/logs")
def get_logs():
    try:
        db: Session = SessionLocal()
        logs = db.query(Log).order_by(Log.timestamp.desc()).limit(50).all()
        return JSONResponse(content={"logs": [log.to_dict() for log in logs]})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
from sqlalchemy.orm import Session
from database import SessionLocal

@app.get("/health/db")
def health_db():
    try:
        db: Session = SessionLocal()
        db.execute("SELECT 1")  # Lightweight DB ping
        db.close()
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": str(e)}
from fastapi import Request
from database import SessionLocal, Log
from datetime import datetime

@app.post("/api/logs")
async def create_log(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "No message")
        timestamp = datetime.now()

        db = SessionLocal()
        new_log = Log(message=message, timestamp=timestamp)
        db.add(new_log)
        db.commit()
        db.close()

        return {"status": "ok", "message": "Log inserted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
