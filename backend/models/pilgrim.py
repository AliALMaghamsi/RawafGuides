from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from db.database import Base
import enum

class Gender(str,enum.Enum):
    male = "male"
    female = "female"

class Pilgrim(Base):
    __tablename__ = "pilgrim"
    id = Column(Integer, primary_key=True , index=True , autoincrement=True)
    name = Column(String(50),nullable=False)
    passport_number = Column(String(50), nullable=False , unique=True)
    assigned_guide_id = Column(ForeignKey("user.id"))
    package_id = Column(ForeignKey("package.id"),nullable=False)
    room_type = Column(Integer , nullable=False)
    assigned_room_id = Column(ForeignKey("room.id"), nullable=True)
    group_id = Column(Integer, nullable=True)
    gender = Column(Enum(Gender), nullable=False)