from pydantic import BaseModel
from typing import Optional


class PillBase(BaseModel):
    name: str
    dosage: str
    manufacturer: str


class PillCreate(PillBase):
    pass  # No additional fields needed for creation


class PillUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[float] = None
    manufacturer: Optional[str] = None


class Pill(PillBase):
    id: int

    class Config:
        orm_mode = True