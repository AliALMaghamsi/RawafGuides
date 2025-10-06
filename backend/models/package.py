from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey  , DATE
from db.database import Base





class Package(Base):
    __tablename__ = "package"
    id = Column(Integer , primary_key=True , index=True , autoincrement=True)
    package_number = Column(String(50) , nullable=False , unique=True)
    
    
    
    hotel1 = Column(String(50), nullable=False)
    check_in_date_h1 = Column(DATE , nullable=False)
    check_out_date_h1 = Column(DATE , nullable=False)
    rooms_2s_h1 = Column(Integer , nullable=False)
    rooms_3s_h1 = Column(Integer,nullable=False)
    rooms_4s_h1 = Column(Integer,nullable=False)
    
   
    
    hotel2 = Column(String(50), nullable=False)
    check_in_date_h2 = Column(DATE , nullable=False)
    check_out_date_h2 = Column(DATE , nullable=False)
    rooms_2s_h2 = Column(Integer , nullable=False)
    rooms_3s_h2 = Column(Integer,nullable=False)
    rooms_4s_h2 = Column(Integer,nullable=False)


    hotel3 = Column(String(50), nullable=True)
    check_in_date_h3 = Column(DATE , nullable=True)
    check_out_date_h3 = Column(DATE , nullable=True)
    rooms_2s_h3 = Column(Integer , nullable=True)
    rooms_3s_h3 = Column(Integer,nullable=True)
    rooms_4s_h3 = Column(Integer,nullable=True)