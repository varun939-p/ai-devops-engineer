import os

reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"
import os

reload_flag = os.getenv("DEV_RELOAD", "false").lower() == "true"

if __name__ == "__main__":
    import uvicorn
    print("[AI-DevOps] Import succeeded - launching FastAPI server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=reload_flag)
