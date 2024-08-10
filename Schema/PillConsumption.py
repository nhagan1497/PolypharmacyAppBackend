from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base class for PillConsumption
class PillConsumptionBase(BaseModel):
    pill_id: int
    quantity: int
    time: Optional[datetime] = None
    user_id: int

# Schema for creating a new PillConsumption
class PillConsumptionCreate(PillConsumptionBase):
    pass  # No additional fields needed for creation

# Schema for updating an existing PillConsumption
class PillConsumptionUpdate(BaseModel):
    pill_id: Optional[int] = None
    quantity: Optional[int] = None
    time: Optional[datetime] = None
    user_id: Optional[int] = None

# Schema for returning PillConsumption data with an ID
class PillConsumption(PillConsumptionBase):
    id: int

    class Config:
        orm_mode = True