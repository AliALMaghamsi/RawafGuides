from pydantic import BaseModel , Field , ConfigDict
from typing import Optional
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    guide = "guide"

class UserBase(BaseModel):
    name:str
    role:Role = Role.guide

class UserUpload(UserBase):
    pass

class UserCreate(UserBase):
    username : str
    hashed_password : str


class UserRead(UserBase):
    id: int
    username:str

    model_config = ConfigDict(from_attributes=True)
    