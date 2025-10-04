from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from db.database import Base
import enum
from passlib import hash

class Role(enum.Enum):
    admin = "admin"
    guide = "guide"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index = True , autoincrement=True)
    name = Column(String(50) , nullable=False)
    passport = Column(String(50), unique=True , nullable=True)
    username = Column(String(50),unique=True , nullable=False)
    hashed_password = Column(String(128),nullable=False)
    role = Column(Enum(Role),default=Role.guide , nullable=False)


