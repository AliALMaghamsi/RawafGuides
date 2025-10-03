from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from db.database import Base
import enum

class Role(enum.Enum):
    admin = "admin"
    guide = "guide"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index = True)
    username = Column(String(50),unique=True , nullable=False)
    hashed_password = Column(String(128),nullable=False)
    role = Column(Enum(Role),default=Role.guide , nullable=False)


class Pilgrim(Base):
    __tablename__ = "pilgrim"
    id = Column(Integer, primary_key=True , index=True)
    name = Column(String(50),nullable=False)
    assigned_guide_id = Column(ForeignKey("user.id"))
    package_id = Column(Integer , nullable=False)
    room_type_id = Column(Integer , nullable=False)
    assigned_room_id = Column(ForeignKey("room.id"), nullable=True)
    Group_id = Column(Integer, nullable=True)


class Package(Base):
    __tablename__ = "package"
    id = Column(Integer , primary_key=True , index=True)
    hotel_name = Column(String(50), nullable=False)
    check_in = Column(DateTime)
    check_out = Column(DateTime)


class RoomType(Base):
    __tablename__ = "room_type"
    id = Column(Integer , primary_key=True)
    capacity = Column(Integer , nullable=False)


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer , primary_key=True , index=True)
    hotel_id = Column(ForeignKey("package.id"))
    check_in = Column(DateTime)
    room_type = Column(ForeignKey("room_type.id"))
    capacity = Column(Integer , nullable=False)
    current_capacity = Column(Integer , default=0 , nullable=False)


    

    

