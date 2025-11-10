# src/etf_service/app/services/holding_service.py
import pandas as pd
import logging
from datetime import date
from fastapi import UploadFile
from sqlalchemy.orm import Session
from etf_service.app.database.session import SessionLocal
from etf_service.app.models.holding_record import HoldingRecord
from etf_service.app.schemas.holding_record import HoldingRecordCreate
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import List

from etf_service.app.logging_config import logger

logger.info("开始插入数据")
executor = ThreadPoolExecutor(max_workers=4)  # 可根据服务器CPU调整

# -----------------------
# 1. Excel解析函数
# -----------------------
# src/etf_service/app/services/holding_service.py
def parse_excel(file: UploadFile) -> List[HoldingRecordCreate]:
    """
    解析上传的 txt 文件（UTF-8编码，制表符分隔）
    """
    import io

    logger.info(f"TXT 文件开始解析: {file.filename}")

    # Step 1: 读取文件内容
    content = file.file.read()
    sample_bytes = content[:200]
    logger.info(f"文件头前200字节: {sample_bytes}")

    # Step 2: 解码为字符串（默认UTF-8）
    try:
        text_io = io.StringIO(content.decode("utf-8"))
    except UnicodeDecodeError:
        logger.warning("UTF-8 解码失败，尝试 GBK")
        text_io = io.StringIO(content.decode("gbk", errors="ignore"))

    # Step 3: 使用 pandas 读取为 DataFrame
    try:
        df = pd.read_csv(
            text_io,
            sep="\t",  # 明确是制表符分隔
            engine="python",
            skip_blank_lines=True
        )
        logger.info(f"TXT 文件解析成功，共 {len(df)} 行，列名: {df.columns.tolist()}")
    except Exception as e:
        logger.error(f"TXT 文件解析失败: {e}")
        raise ValueError(f"无法解析文件: {e}")
    print(df.head())
    
    # Step 4: 清洗列名
    df.columns = [str(c).strip() for c in df.columns]

    # ✅ 清洗数据
    # 1. 把证券代码转为字符串（防止被识别为int）
    if "证券代码" in df.columns:
        df["证券代码"] = df["证券代码"].astype(str)

    # 2. 去掉百分号并转为浮点数
    percent_columns = ["持仓盈亏比例", "当日盈亏比例", "个股仓位"]
    for col in percent_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("%", "", regex=False)
                .replace({"nan": None, "": None})
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")  # 转 float，无法转的设为 NaN

    # 3. 空字符串转为 None
    df = df.replace({r"^\s*$": None}, regex=True)


    # Step 5: 映射为 Pydantic 模型
    records: List[HoldingRecordCreate] = []
    for idx, row in df.iterrows():
        try:
            record_dict = {k: v for k, v in row.to_dict().items() if pd.notna(v)}
            record_dict.setdefault("date", date.today())
            record = HoldingRecordCreate(**record_dict)
            records.append(record)
        except Exception as e:
            logger.warning(f"第 {idx+1} 行解析失败: {e}")
            continue

    logger.info(f"成功解析 {len(records)} 条记录")
    print(records[:3])  # 打印前5条记录以供检查u
    
    return records





# -----------------------
# 2. 单条插入函数
# -----------------------
def insert_record(db: Session, record_in: HoldingRecordCreate) -> HoldingRecord:
    """
    单条数据插入数据库
    """
    record = HoldingRecord(**record_in.dict(by_alias=True))
    p
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# -----------------------
# 3. 批量插入函数（高性能）
# -----------------------
def insert_records_bulk(db: Session, records: List[HoldingRecordCreate]) -> int:
    """
    批量插入，减少commit次数，提高性能
    """
    
    
    orm_records = []
    for r in records:
        record_data = r.dict(by_alias=True)
        orm_record = HoldingRecord(
            date=record_data["date"],
            security_code=record_data["证券代码"],
            security_name=record_data["证券名称"],
            holding_amount=record_data["持仓数量"],
            available_amount=record_data["可用数量"],
            cost_price=record_data["成本价"],
            latest_price=record_data["最新价"],
            holding_profit_ratio=record_data.get("持仓盈亏比例"),
            holding_profit=record_data.get("持仓盈亏"),
            daily_profit_ratio=record_data.get("当日盈亏比例"),
            daily_profit=record_data.get("当日盈亏"),
            avg_buy_price=record_data.get("买入均价"),
            position_ratio=record_data.get("个股仓位"),
            latest_value=record_data.get("最新市值"),
            market=record_data.get("交易市场"),
            shareholder_account=record_data.get("股东账号"),
            currency=record_data.get("币种"),
        )
        orm_records.append(orm_record)
    try:
        db.add_all(orm_records)
        db.commit()
        inserted_count = len(orm_records)
        return inserted_count
    except Exception as e:
        db.rollback()
        logger.error(f"批量插入失败: {e}")
        return 0

# -----------------------
# 4. 异步 Excel 上传处理函数
# -----------------------
async def insert_excel_to_db(file: UploadFile) -> int:
    """
    上传 Excel 文件，解析并批量插入数据库
    使用线程池处理阻塞的数据库操作，支持大文件
    """
    logger.info("开始处理 Excel 上传")
    records = parse_excel(file)
    loop = asyncio.get_running_loop()

    # 每个线程使用独立 Session
    def db_task():
        with SessionLocal() as db:
            return insert_records_bulk(db, records)

    inserted_count = await loop.run_in_executor(executor, db_task)
    return inserted_count
