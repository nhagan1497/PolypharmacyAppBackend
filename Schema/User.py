from pydantic import BaseModel
from typing import Optional

# Base class for User
class UserBase(BaseModel):
    name: str

# Schema for creating a new User
class UserCreate(UserBase):
    pass  # No additional fields needed for creation

# Schema for updating an existing User
class UserUpdate(BaseModel):
    name: Optional[str] = None

# Schema for returning User data with an ID
class User(UserBase):
    uid: int

    class Config:
        orm_mode = True