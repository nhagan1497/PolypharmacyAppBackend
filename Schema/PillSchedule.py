from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base class for PillSchedule
class PillScheduleBase(BaseModel):
    pill_id: int
    quantity: int
    time: datetime
    user_id: int

# Schema for creating a new PillSchedule
class PillScheduleCreate(PillScheduleBase):
    pass  # No additional fields needed for creation

# Schema for updating an existing PillSchedule
class PillScheduleUpdate(BaseModel):
    pill_id: Optional[int] = None
    quantity: Optional[int] = None
    time: Optional[datetime] = None
    user_id: Optional[int] = None

# Schema for returning PillSchedule data with an ID
class PillSchedule(PillScheduleBase):
    id: int

    class Config:
        orm_mode = True