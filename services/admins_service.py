from fastapi import HTTPException, status
from schemas.admins import Admins
from repository.admin_repository import AdminRepository

class AdminsService:
    def __init__(self):
        self.repository = AdminRepository()

    def create_admin(self, admins: Admins):
        try:
            admins.document = int(admins.document)

            admin_data = {
                "name": admins.name,
                "last_name": admins.last_name,
                "document": admins.document
            }

            success = self.repository.create_admin(admin_data)

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya existe",
                )

            return {"message": "El usuario Admin fue regitrado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_all_admins(self):
        try:
            admins = self.repository.get_all_admins()
            return admins
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def update_admin(self, document: int, admins: Admins):
        try:
            admin_data = {}
            if admins.name:
                admin_data["name"] = admins.name
            if admins.last_name:
                admin_data["last_name"] = admins.last_name
            if admins.document:
                admin_data["document"] = int(admins.document)

            success = self.repository.update_admin(document, admin_data)

            if not success:
                raise HTTPException(status_code=404, detail="Administrador no encontrado")

            return {"message": "El usuario administrador fue actualizado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
