from pydantic import BaseModel
from datetime import date
from typing import Optional



class PackageCreate(BaseModel):
    package_number :str
    hotel1 :str
    hotel2 :str
    hotel3 :str
    check_in_date_h1 :date
    check_out_date_h1 :date
    check_in_date_h2 :date
    check_out_date_h2 :date
    check_in_date_h3 :Optional[date] = None
    check_out_date_h3 :Optional[date] = None

class PackageRead(PackageCreate):
    id:int


    class Config:
        orm_mode = True