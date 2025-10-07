from pydantic import BaseModel , Field , ConfigDict
from typing import Optional


class GuideBase(BaseModel):
    name:str = Field(... , min_length=1)
    passport:str = Field(..., min_length=1)

class GuideUPload(GuideBase):
    package_number : str = Field(...,min_length=1)



class GuideDB(GuideUPload):
    username:str
    hashed_password : str
    
    
class GuideRead(GuideBase):
    username: str
    package_id: int
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token : str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None

