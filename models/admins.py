from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from config.database import Base
from datetime import datetime

class Admins(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    document = Column(Integer)
    registry_date = Column(DateTime, default=datetime.now())    

    