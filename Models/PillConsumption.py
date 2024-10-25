from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from base import Base, engine


class PillConsumption(Base):
    __tablename__ = "pill_consumptions"

    id = Column(Integer, primary_key=True, index=True)
    pill_id = Column(Integer)
    quantity = Column(Integer)
    time = Column(DateTime, default=func.now())
    user_id = Column(String)
