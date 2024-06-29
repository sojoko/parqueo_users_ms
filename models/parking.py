from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary
from config.database import Base
from datetime import datetime

class Parking(Base):
    __tablename__ = 'parking'

    id = Column(Integer, primary_key=True)
    user_document = Column(Integer)
    is_in_parking = Column(Integer)
    vehicle_type = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, default=None)

    