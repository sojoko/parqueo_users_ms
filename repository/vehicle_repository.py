from fastapi import HTTPException
from config.database import Session
from models.vehicles import Motocicleta as MotoModel
from models.vehicles import Bicicleta as BiciModel

class VehicleRepository:
    def create_moto(self, moto_data: dict):
        db = Session()
        try:
            new_moto = MotoModel(**moto_data)
            db.add(new_moto)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def create_byci(self, bici_data: dict):
        db = Session()
        try:
            new_bici = BiciModel(**bici_data)
            db.add(new_bici)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_moto_by_user_document(self, document: int):
        db = Session()
        try:
            moto_by_user_document = db.query(MotoModel).filter(MotoModel.user_document == document).first()
            return moto_by_user_document
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_vehicle_by_user_document(self, document: int):
        db = Session()
        try:
            moto_by_user_document = db.query(MotoModel).filter(MotoModel.user_document == document).first()
            bici_by_user_document = db.query(BiciModel).filter(BiciModel.user_document == document).first()
            
            vehicle_for_sent = []
            if moto_by_user_document:
                vehicle_for_sent.append(moto_by_user_document)
            if bici_by_user_document:
                vehicle_for_sent.append(bici_by_user_document)
            
            return vehicle_for_sent
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()