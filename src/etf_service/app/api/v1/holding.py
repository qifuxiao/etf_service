# src/etf_service/app/api/v1/holding.py
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from etf_service.app.services.holding_record_service import (
    insert_excel_to_db, insert_record
)
from etf_service.app.database.session import SessionLocal
from etf_service.app.schemas.holding_record import HoldingRecordCreate, ETFRecordRead
from etf_service.app.logging_config import logger

router = APIRouter(prefix="/holding", tags=["Holding"])

# 依赖注入 Session
def get_db():
    with SessionLocal() as db:
        yield db

# -----------------------
# 上传 Excel
# -----------------------
@router.post("/upload", summary="上传 Excel 并批量插入")
async def upload_excel(file: UploadFile):
    if not file.filename.endswith((".txt")):
        raise HTTPException(status_code=400, detail="文件格式错误")
    try:
        inserted_count = await insert_excel_to_db(file)
        logger.info(f"成功插入 {inserted_count} 条数据")
        return {"inserted_count": inserted_count}
    except Exception as e:
        logger.error(f"Excel 上传失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------
# 单条数据插入
# -----------------------
@router.post("/", response_model=ETFRecordRead, summary="插入单条持仓记录")
def create_holding(record_in: HoldingRecordCreate, db: Session = Depends(get_db)):
    try:
        record = insert_record(db, record_in)
        logger.info(f"插入单条记录: {record_in.dict()}")
        return record
    except Exception as e:
        logger.error(f"单条插入失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
