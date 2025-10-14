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
    
    group_number = Column(Integer, nullable=False)
    gender = Column(Enum(Gender) , nullable=False)
    
    guide_id = Column(ForeignKey("user.id"))
    guide = relationship("User", back_populates="pilgrims")
    
    h1_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    h2_id = Column(Integer, ForeignKey("hotel.id"), nullable=False)
    h3_id = Column(Integer, ForeignKey("hotel.id"), nullable=True)
    
    room_type_h1 = Column(Integer , nullable=False)
    room_type_h2 = Column(Integer , nullable=False)
    room_type_h3 = Column(Integer , nullable=True)

    room_h1_id = Column(Integer, ForeignKey("room.id"), nullable=True)
    room_h2_id = Column(Integer, ForeignKey("room.id"), nullable=True)
    room_h3_id = Column(Integer, ForeignKey("room.id"), nullable=True)

   
    hotel1 = relationship("Hotel", foreign_keys=[h1_id])
    hotel2 = relationship("Hotel", foreign_keys=[h2_id])
    hotel3 = relationship("Hotel", foreign_keys=[h3_id])

    room1 = relationship("Room", foreign_keys=[room_h1_id])
    room2 = relationship("Room", foreign_keys=[room_h2_id])
    room3 = relationship("Room", foreign_keys=[room_h3_id])
