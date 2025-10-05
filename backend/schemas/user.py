from pydantic import BaseModel


class GuideUPload(BaseModel):
    name:str
    passport_number:str
    package_id : int | None = None



class GuideDB(GuideUPload):
    username:str
    hashed_password : str
    
    


class Token(BaseModel):
    access_token : str
    token_type:str

class TokenData(BaseModel):
    username:str|None = None

