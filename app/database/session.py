# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")

# 设置 echo=False 生产中关闭，开发时可 True 便于调试
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
