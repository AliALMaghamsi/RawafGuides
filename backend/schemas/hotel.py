from pydantic import BaseModel , Field , ConfigDict
from typing import Optional



class HotelBase(BaseModel):
    name :str
   


class HotelCreate(HotelBase):
    pass

class HotelRead(HotelBase):
    id:int

    model_config = ConfigDict(from_attributes=True)
    

