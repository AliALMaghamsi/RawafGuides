from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from db.database import Base

class Pilgrim(Base):
    __tablename__ = "pilgrim"
    id = Column(Integer, primary_key=True , index=True , autoincrement=True)
    name = Column(String(50),nullable=False)
    assigned_guide_id = Column(ForeignKey("user.id"))
    package_id = Column(Integer , nullable=False)
    room_type_id = Column(Integer , nullable=False)
    assigned_room_id = Column(ForeignKey("room.id"), nullable=True)
    Group_id = Column(Integer, nullable=True)