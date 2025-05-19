from fastapi import HTTPException
from schemas.vehicles import Motocicletas
from schemas.vehicles import Bicicleta
from repository.vehicle_repository import VehicleRepository

class VehiclesService:
    def __init__(self, repository=None):
        self.repository = repository or VehicleRepository()
    def create_moto(self, motocicletas: Motocicletas):
        try:            
            motocicletas.user_document = int(motocicletas.user_document)   
            vehicle_type = 1

            moto_data = {
                "vehicle_type": vehicle_type,
                "user_document": motocicletas.user_document,
                "placa": motocicletas.placa,
                "marca": motocicletas.marca,
                "modelo": motocicletas.modelo,
                "color": motocicletas.color,
                "foto": motocicletas.foto,         
                "tarjeta_propiedad": motocicletas.tarjeta_propiedad,
                "observaciones": motocicletas.observaciones
            }

            self.repository.create_moto(moto_data)
            return {"message": "La motocicleta fue registrada exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def create_byci(self, bicicleta: Bicicleta):
        try:            
            bicicleta.user_document = int(bicicleta.user_document)   
            vehicle_type = 2

            bici_data = {
                "vehicle_type": vehicle_type,
                "user_document": bicicleta.user_document,
                "numero_marco": bicicleta.numero_marco,
                "marca": bicicleta.marca,
                "modelo": bicicleta.modelo,
                "color": bicicleta.color,
                "foto": bicicleta.foto,         
                "tarjeta_propiedad": bicicleta.tarjeta_propiedad,
                "observaciones": bicicleta.observaciones
            }

            self.repository.create_byci(bici_data)
            return {"message": "La bicileta fue registrada exitosamente"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_moto_by_user_document(self, document: int):
        try:
            moto_by_user_document = self.repository.get_moto_by_user_document(document)        
            if moto_by_user_document is None:
                raise HTTPException(status_code=404, detail="El vehículo no fue encontrado")        
            return moto_by_user_document    
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:    
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_vehicle_by_user_document(self, document: int):
        try:      
            vehicle_for_sent = self.repository.get_vehicle_by_user_document(document)

            if not vehicle_for_sent:
                raise HTTPException(status_code=404, detail="No se encontraron vehículos")

            return vehicle_for_sent

        except HTTPException as http_exc:  
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
