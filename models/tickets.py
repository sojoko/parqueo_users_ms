from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from config.database import Base
from datetime import datetime

class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    document = Column(Integer)   
    vehicle_type = Column(String(20))
    numero_marco = Column(String(50))
    placa = Column(String(50))
    date = Column(DateTime(50))
    description = Column(String(200))
    photo = Column(String(100))
    status = Column(Integer)
    create_date = Column(DateTime, default=datetime.now())
    response_subject = Column(String(100))
    response_body = Column(String(200))
  
    
     