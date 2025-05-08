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
                user_dict['role_id'] = 2
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
            user_dict = aprendiz_by_id.__dict__ if aprendiz_by_id else None
            if user_dict:
                user_dict['role_id'] = 2
            return user_dict
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
                
            aprendiz_status_id = aprendiz.status_id
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
    
    def change_aprendiz_status(self, admin_id: int, status_id: int):
        db = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.id == admin_id).first()
            
            if not aprendiz:
                return False
            
            aprendiz.status_id = status_id
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def update_aprendiz(self, aprendiz_id: int, aprendiz_data: dict):
        db = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.id == aprendiz_id).first()
            print(aprendiz)
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
    
    def get_aprendiz_status_v2(self, page: int, per_page: int):
        db = Session()
        try:
            # Filtrar solo aprendices con status_id 4, 5 o 6
            valid_status_ids = [4, 5, 6]
            # Obtener el total de items que cumplen el criterio para calcular paginación
            total_items = db.query(AprendizModel).filter(AprendizModel.status_id.in_(valid_status_ids)).count()
            
            # Calcular offsets para paginación directamente en la base de datos
            offset = (page - 1) * per_page
            
            # Obtener solo los aprendices de la página actual con los status_id especificados
            aprendices = db.query(AprendizModel).filter(
                AprendizModel.status_id.in_(valid_status_ids)
            ).order_by(AprendizModel.id).offset(offset).limit(per_page).all()
            
            # Recopilar los documentos de los aprendices para buscar sus vehículos
            aprendiz_documents = [aprendiz.document for aprendiz in aprendices]
            
            # Obtener motocicletas y bicicletas solo para los aprendices en la página actual
            motocicletas = db.query(MotocicletaModel).filter(
                MotocicletaModel.user_document.in_(aprendiz_documents)
            ).all() if aprendiz_documents else []
            
            bicicletas = db.query(BicicletaModel).filter(
                BicicletaModel.user_document.in_(aprendiz_documents)
            ).all() if aprendiz_documents else []
            
            # Mapa de vehículos por documento de usuario
            moto_map = {moto.user_document: moto for moto in motocicletas}
            bici_map = {bici.user_document: bici for bici in bicicletas}
            
            # Preparar los resultados incluyendo los vehículos
            aprendices_result = []
            for aprendiz in aprendices:
                aprendiz_dict = aprendiz.__dict__.copy()
                
                # Obtener el estado del aprendiz
                estado = db.query(EstadoAprendiz).filter(EstadoAprendiz.id == aprendiz.status_id).first()
                aprendiz_dict['estado'] = estado.estado if estado else None
                
                # Añadir vehículos
                aprendiz_dict['vehicle'] = []
                
                if aprendiz.document in moto_map:
                    moto = moto_map[aprendiz.document]
                    aprendiz_dict['vehicle'].append({
                        'tipo': 'motocicleta',
                        'placa': moto.placa,
                        'marca': moto.marca,
                        'modelo': moto.modelo,
                        'color': moto.color,
                        'observaciones': moto.observaciones,
                        'foto': moto.foto,
                        'tarjeta_propiedad': moto.tarjeta_propiedad,

                    })
                if aprendiz.document in bici_map:
                    bici = bici_map[aprendiz.document]
                    aprendiz_dict['vehicle'].append({
                        'tipo': 'bicicleta',
                        'marca': bici.marca,
                        'color': bici.color,
                        'modelo': bici.modelo,
                        'numero_marco': bici.numero_marco,
                        'observaciones': bici.observaciones,
                        'foto': bici.foto,
                        'tarjeta_propiedad': bici.tarjeta_propiedad,
                    })
                
                aprendices_result.append(aprendiz_dict)
            
            return {
                "total_items": total_items,
                "page": page,
                "per_page": per_page,
                "items": aprendices_result
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()