from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from sqlalchemy.orm import relationship
from db.database import Base
import enum


class Role(enum.Enum):
    admin = "admin"
    guide = "guide"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index = True , autoincrement=True)
    name = Column(String(50) , nullable=False , unique=True)
    username = Column(String(50),unique=True , nullable=False)
    hashed_password = Column(String(128),nullable=False)
    role = Column(Enum(Role),default=Role.guide , nullable=False)
    
    rooms = relationship("Room" , back_populates="guide")
    pilgrims = relationship("Pilgrim", back_populates="guide", cascade="all, delete-orphan")
    


