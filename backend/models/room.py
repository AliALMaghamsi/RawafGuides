from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from sqlalchemy.orm import relationship
from db.database import Base

class Room(Base):
    __tablename__ = "room"
    
    id = Column(Integer, primary_key=True , index=True , autoincrement=True)
    capacity = Column(Integer, nullable=False)
    current_capacity = Column(Integer, default=0, nullable=False)
    room_number = Column(String, nullable=False)

    hotel_id = Column(ForeignKey("hotel.id"), nullable=False)
    guide_id = Column(ForeignKey("user.id"), nullable=False)

    
    hotel = relationship("Hotel", back_populates="rooms")
    guide = relationship("User",back_populates="rooms")
    pilgrims = relationship("Pilgrim", back_populates="room")
