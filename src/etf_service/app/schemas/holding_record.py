# src/etf_service/app/schemas/holding_record.py
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional
from datetime import date

class BaseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HoldingRecordCreate(BaseSchema):
    date: date
    code: str = Field(..., alias="证券代码")
    name: str = Field(..., alias="证券名称")
    holding_qty: int = Field(..., alias="持仓数量")
    available_qty: int = Field(..., alias="可用数量")
    cost_price: float = Field(..., alias="成本价")
    latest_price: float = Field(..., alias="最新价")
    profit_ratio: Optional[float] = Field(None, alias="持仓盈亏比例")
    profit: Optional[float] = Field(None, alias="持仓盈亏")
    today_profit_ratio: Optional[float] = Field(None, alias="当日盈亏比例")
    today_profit: Optional[float] = Field(None, alias="当日盈亏")
    buy_price: Optional[float] = Field(None, alias="买入均价")
    stock_ratio: Optional[float] = Field(None, alias="个股仓位")
    latest_value: Optional[float] = Field(None, alias="最新市值")
    market: Optional[str] = Field(None, alias="交易市场")
    shareholder_account: Optional[str] = Field(None, alias="股东账号")
    currency: Optional[str] = Field(None, alias="币种")

    model_config = ConfigDict(
        populate_by_name=True,   # ✅ 替代 allow_population_by_field_name
        from_attributes=True     # ✅ 替代 orm_mode
    )

class ETFRecordRead(HoldingRecordCreate):
    id: int

    class Config:
        orm_mode = True
