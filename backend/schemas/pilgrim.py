from pydantic import BaseModel, Field , ConfigDict
from typing import Optional
from enum import Enum

class Gender(str,Enum):
    male = "male"
    female = "female"


class PilgrimBase(BaseModel):
    name: str = Field(..., min_length=1)
    gender: Gender
    room_type: int = Field(..., ge=2, le=4)
    group_number: Optional[int] = None

class PilgrimCreate(PilgrimBase):
    guide_name: str  
    room_id: Optional[int] = None


class PilgrimUpdateRoom(BaseModel):
    room_id: Optional[int] = Field(None)

    model_config = ConfigDict(from_attributes=True)

class PilgrimRead(PilgrimBase):
    guide_id : int
    room_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)