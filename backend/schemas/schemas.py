from pydantic import BaseModel
from enum import Enum

class Role(str , Enum):
    admin = "admin"
    guide = "guide"



class UserCreate(BaseModel):

    user:str
    password : str
    role : Role = Role.guide

class UserOut(BaseModel):
    id:int
    user: str
    role : Role


class PilgrimCreate(BaseModel):
    id:int
    name:str
    assigned_guide_id : int
    
