from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class GenderEnum(str,Enum):
    male = "male"
    female = "female"


class PilgrimCreate(BaseModel):
   
    name: str = Field(... , min_length=1)
    passport_number:str = Field(...)
    assigned_guide_passport:str = Field(...)
    package_number:str = Field(...)
    room_type :int = Field(...)
    group_id:Optional[int]=None
    gender:GenderEnum


    

class PilgrimRead(PilgrimCreate):
    id:int


class PilgrimUpdate(BaseModel):
    assigned_room_id : str = Field(...)