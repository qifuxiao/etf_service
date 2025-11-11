from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from etf_service.app.database.session import SessionLocal
from etf_service.app.models.holding_record import HoldingRecord
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/holding", tags=["holding"])

class HoldingChartData(BaseModel):
    date: str
    holding_qty: float
    cost_price: float

def get_db():
    with SessionLocal() as db:
        yield db

@router.get("/chart/{security_code}", response_model=List[HoldingChartData])
def get_holding_chart(security_code: str, db: Session = Depends(get_db)):
    records = (
        db.query(HoldingRecord)
        .filter(HoldingRecord.security_code == int(security_code))
        .order_by(HoldingRecord.date)
        .all()
    )
    if not records:
        raise HTTPException(status_code=404, detail="No data found")
    return [
        HoldingChartData(
            date=r.date.isoformat(),
            holding_qty=r.holding_amount,
            cost_price=r.cost_price
        )
        for r in records
    ]

@router.get("/security-codes", response_model=List[str])
def get_security_codes(db: Session = Depends(get_db)):
    """
    返回数据库中所有证券代码，用于前端选择下拉列表
    """
    codes = db.query(HoldingRecord.security_code).distinct().all()
    # db 返回的是 list of tuples，需要展开成 list[str]
    return [str(code[0]) for code in codes]