from pydantic import BaseModel
from datetime import date
from typing import Optional



class PackageCreate(BaseModel):
    package_number :str

    hotel1 :str
    check_in_date_h1 :date
    check_out_date_h1 :date
    rooms_2s_h1 : int
    rooms_3s_h1 : int
    rooms_4s_h1 : int
    
    hotel2 :str
    check_in_date_h2 :date
    check_out_date_h2 :date
    rooms_2s_h2 : int
    rooms_3s_h2 : int
    rooms_4s_h2 : int
    
    hotel3 :Optional[str]= None
    check_in_date_h3 :Optional[date] = None
    check_out_date_h3 :Optional[date] = None
    rooms_2s_h3 : Optional[int] = None
    rooms_3s_h3 : Optional[int] = None
    rooms_4s_h3 : Optional[int] = None

class PackageRead(PackageCreate):
    id:int


    class Config:
        from_attributes = True