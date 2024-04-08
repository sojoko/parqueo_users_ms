from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from config.database import Base
from datetime import datetime
from models.aprendices import Aprendices
#from passlib.context import CryptContext

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    document = Column(Integer)
    password = Column(String(50))
    state_id = Column(Integer, ForeignKey('user_status.id')) 
    roll_id = Column(Integer, ForeignKey('user_roll.id')) 

class UserStatus(Base):
    __tablename__ = 'user_status'

    id = Column(Integer, primary_key=True)
    estado = Column(String(50))
    
class UserRoll(Base):
    __tablename__ = 'user_roll'

    id = Column(Integer, primary_key=True)
    estado = Column(String(50))
    