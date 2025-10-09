from models.user import User
from sqlalchemy.orm import Session
from models.user import User

from fastapi import HTTPException , status


def get_user_by_username(db : Session , username :str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db:Session , user_id :int):
    return db.query(User).filter(User.id == user_id).one_or_none()


def get_guide_id_by_passport(db:Session , passport_number:str):
    guide_id= db.query(User).filter(User.passport == passport_number).first()
    if not guide_id:
        return None
    return guide_id.id
