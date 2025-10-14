from pydantic import BaseModel, Field , ConfigDict , computed_field
from typing import Optional
from enum import Enum

class Gender(str,Enum):
    male = "male"
    female = "female"


class PilgrimBase(BaseModel):
    name: str = Field(..., min_length=1)
    gender: Gender
    passport_number:str
    room_type_h1: int = Field(..., ge=2, le=4)
    room_type_h2: int = Field(..., ge=2, le=4)
    room_type_h3: Optional[int] = Field(default=None, ge=2, le=4)
    
    group_number: int

class PilgrimCreate(PilgrimBase):
    guide_name: str
    h1_name :str
    h2_name :str
    h3_name :Optional[str]= None  
    room_h1_id: Optional[int] = None
    room_h2_id: Optional[int] = None
    room_h3_id: Optional[int] = None


class PilgrimUpdateRoom(BaseModel):
    room_id: Optional[int] = None

class PilgrimRead(PilgrimBase):
    id:int
    guide_id : int
    h1_id: int
    h2_id: int
    h3_id: int | None = None
    room_h1_id: Optional[int] = None
    room_h2_id: Optional[int] = None
    room_h3_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
    
    @computed_field
    def is_assigned(self) -> bool:
        return any([self.room_h1_id, self.room_h2_id, self.room_h3_id])
    
    