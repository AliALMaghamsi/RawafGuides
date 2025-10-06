from pydantic import BaseModel , Field


class GuideUPload(BaseModel):
    name:str = Field(... , min_length=1)
    passport_number:str = Field(..., min_length=1)
    package_number : str = Field(...,min_length=1)



class GuideDB(GuideUPload):
    username:str
    hashed_password : str
    
    
class GuideRead(GuideUPload):
    username: str
    id: int



class Token(BaseModel):
    access_token : str
    token_type:str

class TokenData(BaseModel):
    username:str|None = None

