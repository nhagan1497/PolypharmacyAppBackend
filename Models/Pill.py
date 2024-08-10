from sqlalchemy import Column, Integer, String, Float
from base import Base


class Pill(Base):
    __tablename__ = "pills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    dosage = Column(Float)
    manufacturer = Column(String, index=True)