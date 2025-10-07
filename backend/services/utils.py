from models.user import User
from sqlalchemy.orm import Session
from models.user import User
from models.package import Package


def get_user_by_username(db : Session , username :str):
    return db.query(User).filter(User.username == username).first()


def get_guide_id_by_passport(db:Session , passport_number:str):
    guide_id= db.query(User).filter(User.passport == passport_number).first()
    return guide_id.id

def get_package_id_by_number(db:Session , package_number:str):
    package_id = db.query(Package).filter(Package.package_number == package_number).first()
    return package_id.id