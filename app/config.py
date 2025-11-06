# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./tmp/uploads")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))

# 可选：用于测试或调试
if __name__ == "__main__":
    print("✅ Configuration loaded:")
    print(f"DATABASE_URL: {DATABASE_URL}")
    print(f"APP_HOST: {APP_HOST}")
    print(f"APP_PORT: {APP_PORT}")
    print(f"UPLOAD_DIR: {UPLOAD_DIR}")
    print(f"MAX_UPLOAD_SIZE: {MAX_UPLOAD_SIZE} bytes")