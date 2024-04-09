from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from config.database import Base
from datetime import datetime

class Motocicleta(Base):
    __tablename__ = 'motocicleta'

    id = Column(Integer, primary_key=True)    
    user_document = Column(Integer)
    placa = Column(String(50))
    marca = Column(String(50))
    modelo = Column(String(50))
    color = Column(String(50))
    foto = Column(String(100))
    soat = Column(String(100))
    tarjeta_propiedad = Column(String(100))
    observaciones = Column(String(200))
    registry_date = Column(DateTime, default=datetime.now)
  


class Bicicleta(Base):
    __tablename__ = 'bicicleta'

    id = Column(Integer, primary_key=True)    
    user_document = Column(Integer)
    numero_marco = Column(String(50))
    marca = Column(String(50))
    modelo = Column(String(50))
    color = Column(String(50))
    foto = Column(String(100)) 
    tarjeta_propiedad = Column(String(100))
    observaciones = Column(String(200))
    registry_date = Column(DateTime, default=datetime.now)
  