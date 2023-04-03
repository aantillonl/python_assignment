from datetime import date

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Integer


class Base(DeclarativeBase):
    pass

class FinancialData(Base):
    __tablename__ = "financial_data"
    id = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(5))
    date: Mapped[date]
    open_price: Mapped[float]
    close_price: Mapped[float]
    volume: Mapped[int]
    
    __table_args__ = (
        UniqueConstraint("symbol", "date"),
    )
