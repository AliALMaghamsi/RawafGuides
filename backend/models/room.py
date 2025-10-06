from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from db.database import Base

class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True , index=True , autoincrement=True)
    package_id = Column(ForeignKey("package.id"), nullable=False)
    hotel_name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    current_capacity = Column(Integer, default=0, nullable=False)
    room_number = Column(String, nullable=False)
    