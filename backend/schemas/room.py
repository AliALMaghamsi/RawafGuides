from pydantic import BaseModel , Field
from typing import Optional




class RoomCreate(BaseModel):
    hotel_name : str = Field(...)
    package_id:str =Field(...)
    room_name:str = Field(...)
    capacity:int = Field(...)
    current_capacity:int = Field(...,default=0)


class RoomRead(RoomCreate):
    id:int