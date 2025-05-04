from fastapi import HTTPException
from datetime import datetime
from config.database import Session
from fastapi.encoders import jsonable_encoder
from models.aprendices import Aprendices as AprendizModel
from models.aprendices import EstadoAprendiz
from models.vehicles import Motocicleta as MotocicletaModel
from models.vehicles import Bicicleta as BicicletaModel

class AprendizRepository:
    def get_all_aprendices(self):
        db = Session()
        try:
            aprendinces = db.query(AprendizModel).all()
            aprendices_with_roll = []
            for user in aprendinces:
                user_dict = user.__dict__
                user_dict['roll'] = "aprendiz"
                aprendices_with_roll.append(user_dict)
            return aprendices_with_roll
        finally:
            db.close()
    
    def create_aprendiz(self, aprendiz_data):
        db = Session()
        try:
            aprendiz_exist = db.query(AprendizModel).filter(AprendizModel.document == aprendiz_data["document"]).first()
            if aprendiz_exist:
                return False
            
            new_aprendiz = AprendizModel(**aprendiz_data)
            db.add(new_aprendiz)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_aprendiz_by_id(self, id: int):
        db = Session()
        try:      
            aprendiz_by_id = db.query(AprendizModel).filter(AprendizModel.id == id).first()       
            return aprendiz_by_id
        except Exception as e:        
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def get_aprendiz_by_document(self, document: int):
        db = Session()
        try:
            aprendiz_by_document = db.query(AprendizModel).filter(AprendizModel.document == document).first()
            return aprendiz_by_document
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_aprendiz_status_by_document(self, document: int):
        db = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()
            if not aprendiz:
                return None
                
            aprendiz_status_id = aprendiz.state_id 
            status = db.query(EstadoAprendiz).filter(EstadoAprendiz.id == aprendiz_status_id).first()        
            return status.estado if status else None
        except Exception as e:     
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def get_aprendiz_status(self, page: int, per_page: int):
        db = Session()
        try:
            aprendices = db.query(AprendizModel).all()
            motocicletas = db.query(MotocicletaModel).all()
            bicicletas = db.query(BicicletaModel).all()
            
            aprendices_dict = {aprendiz.document: aprendiz for aprendiz in aprendices}
            
            for motocicleta in motocicletas:
                if motocicleta.user_document in aprendices_dict:
                    aprendiz = aprendices_dict[motocicleta.user_document]
                    aprendiz.vehicle = motocicleta
            
            for bicicleta in bicicletas:
                if bicicleta.user_document in aprendices_dict:
                    aprendiz = aprendices_dict[bicicleta.user_document]
                    aprendiz.vehicle = bicicleta
            
            aprendices_combined = list(aprendices_dict.values())
            total_items = len(aprendices_combined)
            start = (page - 1) * per_page
            end = start + per_page
            aprendices_paginated = aprendices_combined[start:end]
            
            return {
                "total_items": total_items,
                "page": page,
                "per_page": per_page,
                "items": aprendices_paginated
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_aprendiz_with_vehicles(self, document: int):
        db = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()    
            vehicles = db.query(MotocicletaModel).filter(MotocicletaModel.user_document == document).all()
            
            aprendiz_dict = jsonable_encoder(aprendiz) if aprendiz else {}
            vehicles_list = jsonable_encoder(vehicles) if vehicles else []
            
            vehicles_dict = {"vehicle_" + str(i): vehicle for i, vehicle in enumerate(vehicles_list)}
            
            response_data = {**aprendiz_dict, **vehicles_dict}
            
            return response_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def change_aprendiz_status(self, document: int, state_id: int):
        db = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()
            
            if not aprendiz:
                return False
            
            aprendiz.state_id = state_id
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def update_aprendiz(self, document: int, aprendiz_data: dict):
        db = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()        
            if not aprendiz:
                return False
                
            for key, value in aprendiz_data.items():
                setattr(aprendiz, key, value)
                
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()