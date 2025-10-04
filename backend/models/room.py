from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from db.database import Base

class RoomType(Base):
    __tablename__ = "room_type"
    id = Column(Integer , primary_key=True , autoincrement=True)
    capacity = Column(Integer , nullable=False)


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer , primary_key=True , index=True , autoincrement=True)
    hotel_id = Column(ForeignKey("package.id"))
    check_in = Column(DateTime)
    room_type = Column(ForeignKey("room_type.id"))
    capacity = Column(Integer , nullable=False)
    current_capacity = Column(Integer , default=0 , nullable=False)
