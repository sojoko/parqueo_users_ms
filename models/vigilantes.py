from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from config.database import Base
from datetime import datetime

class Vigilantes(Base):
    __tablename__ = 'vigilantes'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    document = Column(Integer)   
    registry_date = Column(DateTime, default=datetime.now())
    status_id = Column(Integer, ForeignKey("status_vigilante.id"))
  
class VigilanteStatus(Base):
    __tablename__ = 'status_vigilante'

    id = Column(Integer, primary_key=True)
    status = Column(String(50))
