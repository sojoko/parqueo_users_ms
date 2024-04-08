from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary
from config.database import Base
from datetime import datetime

class QR(Base):
    __tablename__ = 'qr'

    id = Column(Integer, primary_key=True)
    qr_image = Column(LargeBinary)
    user_document = Column(Integer)   
    registry_date = Column(DateTime, default=datetime.now())

    