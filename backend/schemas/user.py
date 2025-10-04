from pydantic import BaseModel


class GuideUPload(BaseModel):
    name:str
    passport_number:str


class GuideDB(BaseModel):
    id:int
    name:str
    username:str
    passport_number:str

