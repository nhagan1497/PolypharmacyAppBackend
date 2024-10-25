from sqlalchemy import Column, Integer, String
from base import Base, engine


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    name = Column(String)
