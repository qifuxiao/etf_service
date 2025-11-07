# app/main.py
from fastapi import FastAPI
from etf_service.logging_config import setup_logging
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from etf_service.config import UPLOAD_DIR

setup_logging()
app = FastAPI(title="etf_ingest_service")

# Ensure upload dir exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static/templates later when we add frontend files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
# templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def root():
    return {"message": "etf_ingest_service running"}
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")