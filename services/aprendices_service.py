from datetime import datetime
from fastapi import HTTPException
from schemas.aprendices import Aprendices, ChangeStatusRequest
from repository.aprendiz_repository import AprendizRepository

class AprendicesService:
    def __init__(self):
        self.repository = AprendizRepository()

    def get_all_aprendices(self):
        return self.repository.get_all_aprendices()

    def create_aprendiz(self, aprendices: Aprendices):
        try:
            finish_date = datetime.strptime(aprendices.finish_date, "%Y-%m-%d")        
            status_default = 1
            aprendices.document = int(aprendices.document)
            aprendices.ficha = int(aprendices.ficha)

            aprendiz_data = {
                "name": aprendices.name,
                "last_name": aprendices.last_name,
                "document": aprendices.document,
                "ficha": aprendices.ficha,
                "photo": aprendices.photo,
                "email": aprendices.email,     
                "finish_date": finish_date,
                "state_id": status_default
            }

            success = self.repository.create_aprendiz(aprendiz_data)

            if not success:
                raise HTTPException(status_code=400, detail="El documento ya existe")

            return {"message": "El aprendiz fue registrado exitosamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_aprendiz_by_id(self, id: int):
        try:      
            aprendiz_by_id = self.repository.get_aprendiz_by_id(id)       
            if aprendiz_by_id is None:
                raise HTTPException(status_code=404, detail="El aprendiz no fue encontrado")        
            return aprendiz_by_id
        except HTTPException as http_exc:      
            raise http_exc
        except Exception as e:        
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    

    def get_aprendiz_by_document(self, document: int):
        try:
            aprendiz_by_document = self.repository.get_aprendiz_by_document(document)
            if aprendiz_by_document is None:
                raise HTTPException(status_code=404, detail="El documento no fue encontrado")
            return aprendiz_by_document
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_aprendiz_status_by_document(self, document: int):
        try:
            status = self.repository.get_aprendiz_status_by_document(document)

            if status is None:
                raise HTTPException(status_code=404, detail="El documento no fue encontrado o el estado no existe")

            return status
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:     
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_aprendiz_status(self, page: int, per_page: int):
        try:
            result = self.repository.get_aprendiz_status(page, per_page)

            if not result.get("items"):
                raise HTTPException(status_code=404, detail="No hay aprendices en esta página")

            return result
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_aprendiz_with_vehicles(self, document: int):
        try:
            response_data = self.repository.get_aprendiz_with_vehicles(document)
            return response_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def change_aprendiz_status(self, req: ChangeStatusRequest):
        try:
            document = int(req.document)
            state_id = int(req.state_id)

            success = self.repository.change_aprendiz_status(document, state_id)

            if not success:
                raise HTTPException(status_code=404, detail="El documento no fue encontrado")

            return {"message": "El estado del aprendiz fue actualizado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def update_aprendiz(self, document: int, aprendices: Aprendices):
        try:
            aprendiz_data = {}
            if aprendices.name:
                aprendiz_data["name"] = aprendices.name
            if aprendices.last_name:
                aprendiz_data["last_name"] = aprendices.last_name
            if aprendices.document:
                aprendiz_data["document"] = int(aprendices.document)
            if aprendices.ficha:
                aprendiz_data["ficha"] = int(aprendices.ficha)
            if aprendices.email:
                aprendiz_data["email"] = aprendices.email

            success = self.repository.update_aprendiz(document, aprendiz_data)

            if not success:
                raise HTTPException(status_code=404, detail="Aprendiz no encontrado")

            return {"message": "El aprendiz fue actualizado correctamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
