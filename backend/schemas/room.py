from pydantic import BaseModel , Field , ConfigDict
from typing import Optional




class RoomBase(BaseModel):
    hotel_id : int
    guide_id :int
    room_number : str
    capacity:int
    current_capacity:int = 0

class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id : int 

    model_config = ConfigDict(from_attributes=True)
    