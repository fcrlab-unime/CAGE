import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from utils import save_to_csv

# Load .env
load_dotenv()

CSV_FILE = os.getenv("CSV_FILE", "notifications.csv")
HOST = os.getenv("SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("SERVER_PORT", 9999))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(title="Server KPI FastAPI")

@app.get("/server-kpi/ping")
async def ping():
    return {"status": "ok"}

@app.post("/server-kpi/notify")
async def receive_notification(request: Request):
    try:
        data = await request.json()
        raw_body = await request.body()

        save_to_csv(data, raw_body, CSV_FILE)

        return JSONResponse(
            {"status": "success", "message": "Notification received and saved!"},
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=400
        )
