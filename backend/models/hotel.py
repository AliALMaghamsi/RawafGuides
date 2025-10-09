from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from sqlalchemy.orm import relationship
from db.database import Base



class Hotel(Base):
    __tablename__ = "hotel"

    id = Column(Integer , primary_key=True , index=True , autoincrement=True)
    name = Column(String(50), unique=True , nullable=False)
    
    rooms = relationship("Room", back_populates="hotel")
