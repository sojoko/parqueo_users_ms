from fastapi import HTTPException
from schemas.vigilantes import Vigilantes, ChangeStatusRequest
from repository.vigilante_repository import VigilanteRepository

class VigilanteService:
    def __init__(self, repository=None):
        self.repository = repository or VigilanteRepository()

    def create_vigilante(self, vigilantes: Vigilantes):
        try:
            success = self.repository.create_vigilante(vigilantes)

            if not success:
                raise HTTPException(status_code=400, detail="El documento ya está registrado")

            return {"message": "El usuario vigilante fue registrado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def update_vigilante(self, document: int, vigilantes: Vigilantes):
        try:
            result = self.repository.update_vigilante(document, vigilantes)

            if not result:
                raise HTTPException(status_code=404, detail="Vigilante no encontrado")

            return {"message": "El usuario vigilante fue actualizado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_vigilante_by_id(self, id: int):
        try:
            vigilante = self.repository.get_vigilante_by_id(id)

            if not vigilante:
                raise HTTPException(status_code=404, detail="Vigilante no encontrado")

            return vigilante
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_vigilante_by_document(self, document: int):
        try:
            vigilante = self.repository.get_vigilante_by_document(document)

            if not vigilante:
                raise HTTPException(status_code=404, detail="Vigilante no encontrado")

            return vigilante
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_all_vigilant(self, page: int, per_page: int):
        try:
            skip = (page - 1) * per_page
            return self.repository.get_all_vigilant(skip, per_page)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def change_vigilante_status(self, request: ChangeStatusRequest):
        try:
            result = self.repository.change_vigilante_status(request)

            if not result:
                raise HTTPException(status_code=404, detail="El vigilante no fue encontrado")

            return {"message": "El estado del vigilante fue actualizado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
