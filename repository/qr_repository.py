import httpx
from datetime import datetime, timedelta
from config.database import Session
from fastapi import HTTPException
from models.qr import QR as QRModel
from models.parking import Parking as ParkingModel
from base64 import b64encode

class QRRepository:
    def get_qr_by_document(self, document: int):
        db = Session()
        try:
            qr = db.query(QRModel).filter(QRModel.user_document == document).first()
            return qr
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_last_qr_by_document(self, document: int):
        db = Session()
        try:
            last_qr = db.query(QRModel).filter(QRModel.user_document == document).order_by(QRModel.registry_date.desc()).first()
            return last_qr
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def create_qr(self, qr_data: dict):
        db = Session()
        try:
            new_qr = QRModel(**qr_data)
            db.add(new_qr)
            db.commit()
            
            # Get the newly created QR code
            qr_code_generated = db.query(QRModel).filter(QRModel.user_document == qr_data["user_document"]).order_by(QRModel.registry_date.desc()).first().qr_image
            qr_code_generated_binary = b64encode(qr_code_generated).decode('utf-8')
            
            return qr_code_generated_binary
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_all_parking(self):
        db = Session()
        try:
            parking = db.query(ParkingModel).all()
            return parking
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()