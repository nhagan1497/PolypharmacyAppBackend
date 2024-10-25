from sqlalchemy import Column, Integer, String, Float
from base import Base, engine


class Pill(Base):
    __tablename__ = "pills"

    id = Column(Integer, primary_key=True, index=True, )
    name = Column(String)
    dosage = Column(String)
    manufacturer = Column(String)
    user_id = Column(String)
