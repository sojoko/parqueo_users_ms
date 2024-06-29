from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from config.database import Base
from datetime import datetime

class Aprendices(Base):
    __tablename__ = 'aprendices'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    document = Column(Integer)
    ficha = Column(Integer)
    email = Column(String(50))
    photo = Column(String(100))
    registry_date = Column(DateTime, default=datetime.now)
    finish_date = Column(DateTime)
    state_id = Column(Integer, ForeignKey('status_aprendiz.id'))

class EstadoAprendiz(Base):
    __tablename__ = 'status_aprendiz'

    id = Column(Integer, primary_key=True)
    estado = Column(String(50))
    
    
