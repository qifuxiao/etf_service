# app/main.py
from fastapi import FastAPI
from etf_service.app.logging_config import logger
from etf_service.app.logging_config import setup_logging
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import os
from etf_service.config import UPLOAD_DIR
from etf_service.app.api.v1 import holding

setup_logging()
app = FastAPI(title="etf_ingest_service")

# 注册 v1 路由
app.include_router(holding.router, prefix="/api/v1")

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
    return FileResponse("../static/favicon.ico")

# 示例路由
@app.get("/ping")
async def ping():
    logger.info("Ping 请求被调用")  # 使用全局 logger
    return {"message": "pong"}