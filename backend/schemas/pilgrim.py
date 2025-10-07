from pydantic import BaseModel, Field , ConfigDict
from typing import Optional
from enum import Enum

class GenderEnum(str,Enum):
    male = "male"
    female = "female"

class PilgrimBase(BaseModel):
    name: str = Field(... , min_length=1)
    passport_number:str = Field(...)
    room_type :int = Field(...)
    group_id:Optional[int]=None
    gender:GenderEnum

class PilgrimCreate(PilgrimBase):
   
    
    assigned_guide_passport:str = Field(...)
    package_number:str = Field(...)
    


    

class PilgrimRead(PilgrimBase):
    id:int
    assigned_guide_id : int 
    package_id : int

    model_config = ConfigDict(from_attributes=True)


class PilgrimUpdate(BaseModel):
    assigned_room_id : str = Field(...)