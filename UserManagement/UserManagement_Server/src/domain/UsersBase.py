from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    role: Optional[str] = None
    password: str

#class for create user
class UserCreate(UserBase):
  pass