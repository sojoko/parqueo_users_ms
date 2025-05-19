from datetime import datetime
from fastapi import HTTPException, status
from schemas.parking import Parking
from repository.parking_repository import ParkingRepository

class ParkingService:
    def __init__(self, repository=None):
        self.repository = repository or ParkingRepository()
    def create_parking(self, parking: Parking):
        try:
            parking.user_document = int(parking.user_document)

            parking_data = {
                "user_document": parking.user_document,
                "is_in_parking": parking.is_in_parking,
                "vehicle_type": parking.vehicle_type
            }

            success = self.repository.create_parking(parking_data)

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un registro para este usuario en el parqueadero",
                )

            return {"message": "El movimiento fue regitrado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_all_parking(self):
        try:      
            return self.repository.get_all_parking()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_all_parking_counter(self):
        try:
            return self.repository.get_all_parking_counter()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_parking_by_document(self, user_document: int):
        try:      
            return self.repository.get_parking_by_document(user_document)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def update_parking(self, user_document: int, parking: Parking):
        try:
            parking_data = {
                "is_in_parking": parking.is_in_parking
            }

            success = self.repository.update_parking(user_document, parking_data)

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontró un registro de parqueo para este usuario"
                )

            return {"message": "El registro de parqueo fue actualizado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
