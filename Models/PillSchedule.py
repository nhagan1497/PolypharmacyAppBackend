from sqlalchemy import Column, Integer, String, Float, Time
from base import Base, engine


class PillSchedule(Base):
    __tablename__ = "pill_schedules"

    id = Column(Integer, primary_key=True, index=True)
    pill_id = Column(Integer)
    quantity = Column(Integer)
    time = Column(Time)
    user_id = Column(String)


Base.metadata.create_all(bind=engine)