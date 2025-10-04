from sqlalchemy import Boolean,Column,Integer,String,Enum,ForeignKey , DateTime
from db.database import Base





class Package(Base):
    __tablename__ = "package"
    id = Column(Integer , primary_key=True , index=True , autoincrement=True)
    package_number = Column(Integer , nullable=False , unique=True)

    hotel1 = Column(String(50), nullable=False)
    hotel2 = Column(String(50), nullable=False)
    hotel1 = Column(String(50), nullable=True)
    check_in_date_h1 = Column(DateTime , nullable=False)
    check_out_date_h1 = Column(DateTime , nullable=False)
    check_in_date_h2 = Column(DateTime , nullable=False)
    check_out_date_h2 = Column(DateTime , nullable=False)
    check_in_date_h3 = Column(DateTime , nullable=True)
    check_out_date_h3 = Column(DateTime , nullable=True)