import os

reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"
uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=reload_flag)
if __name__ == "__main__":
    import uvicorn
    print("[AI-DevOps] Import succeeded - launching FastAPI server...")
    import os; reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"; import os`nreload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"`nimport os
reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"
import os
reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"
import os
reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"
uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=reload_flag)
@app.get("/health/db")
def health_db():
    try:
        # TODO: Replace with your real DB connectivity check
        return {"status": "ok", "db": "healthy"}
    except Exception as e:
        return {"status": "error", "db": str(e)}
@app.get("/health/db")
def health_db():
    try:
        # TODO: Replace with your real DB connectivity check
        return {"status": "ok", "db": "healthy"}
    except Exception as e:
        return {"status": "error", "db": str(e)}
def ping():
    return {"status": "ok", "message": "pong"}
def ping():
    return {"status": "ok", "message": "pong"}
def ping():
    return {"status": "ok", "message": "pong"}
def ping():
    return {"status": "ok", "message": "pong"}
def ping():
    return {"status": "ok", "message": "pong"}
def ping():
    return {"status": "ok", "message": "pong"}
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}
