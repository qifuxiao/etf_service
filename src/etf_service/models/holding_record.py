from sqlalchemy import Column,Date, Float, ForeignKey, Integer, String
from etf_service.database.base import Base, TimestampMixin

class HoldingRecord(Base,TimestampMixin):
        """
        每日ETF/股票持仓记录
        记录某ETF在特定日期的持仓详情
        """
        __tablename__ = "holding_record"
        
        id = Column(Integer, primary_key=True, index=True)
        date = Column(Date,nullable=False, index=True,comment="持仓日期")
        
        security_code = Column(Integer,nullable=False, index=True, comment="证券代码")  
        security_name = Column(String(100),nullable=False, comment="证券名称")

        holding_amount = Column(Float,nullable=False, comment="持仓数量")
        available_amount = Column(Integer,nullable=False, comment="可用数量")

        cost_price = Column(Float,nullable=False, comment="持仓成本价")
        latest_price = Column(Float,nullable=False, comment="最新价")
        
        holding_profit_ratio = Column(Float, comment="持仓盈亏比例（%）")
        holding_profit = Column(Float, comment="持仓盈亏金额")

        daily_profit_ratio = Column(Float, comment="当日盈亏比例（%）")
        daily_profit = Column(Float, comment="当日盈亏金额")

        avg_buy_price = Column(Float, comment="买入均价")
        position_ratio = Column(Float, comment="个股仓位（%）")

        latest_value = Column(Float, comment="最新市值")
        market = Column(String(50), comment="交易市场")
        shareholder_account = Column(String(50), comment="股东账号")
        currency = Column(String(20), comment="币种")
