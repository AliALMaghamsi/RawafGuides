from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from sqlalchemy.orm import relationship
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
    room_type = Column(Integer , nullable=False)
    group_number = Column(Integer, nullable=True)
    gender = Column(Enum(Gender) , nullable=False)
    room_id = Column(ForeignKey("room.id"), nullable=True)
    guide_id = Column(ForeignKey("user.id"))

    guide = relationship("User", back_populates="pilgrims")
    room = relationship("Room", back_populates="pilgrims")
