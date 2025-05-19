from fastapi import HTTPException, status
from schemas.usersLogin import User
from schemas.usersRegistry import UserRegistry
from jwt_manager import create_tokens
from fastapi.encoders import jsonable_encoder
from repository.user_repository import UserRepository
import bcrypt

class UsersService:
    def __init__(self, repository=None):
        self.repository = repository or UserRepository()
    def get_user(self, document: int):
        user = self.repository.get_user_by_document(document)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

    def delete_user(self, document: int, roll: int):
        if roll not in [1, 2, 3]:
            raise HTTPException(status_code=400, detail="Rol no válido")

        success = self.repository.delete_user_by_document_and_roll(document, roll)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"message": "Usuario eliminado con éxito"}

    def get_user_all(self):
        users = self.repository.get_all_users()
        if not users:
            raise HTTPException(status_code=404, detail="No se encontraron usuarios")
        return users

    def login(self, users: User):
        try:
            users.password = str(users.password)
            users.document = int(users.document)

            user = self.repository.get_user_by_document_with_password(users.document)

            if not user or not bcrypt.checkpw(users.password.encode('utf-8'), user.password.encode('utf-8')):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario o contraseña incorrectos",
                )

            roll = user.roll_id
            name = None

            if roll == 1:
                name = self.repository.get_admin_name_by_document(users.document)
            elif roll == 2:
                name = self.repository.get_aprendiz_name_by_document(users.document)
            elif roll == 3:
                name = self.repository.get_vigilante_name_by_document(users.document)

            if name is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontró el nombre del usuario",
                )

            user_for_token = {"document": user.document, "password": user.password}
            access_token, refresh_token = create_tokens(data=user_for_token)

            return {
                "name": name,
                "document": users.document,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user_roll": roll
            }
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def create_user(self, users: UserRegistry):
        try:
            users.password = str(users.password)
            users.document = str(users.document)
            status_default = 1

            hashed_password = bcrypt.hashpw(users.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user_data = {
                "document": users.document,
                "password": hashed_password,
                "state_id": status_default,
                "roll_id": users.roll_id,
            }

            success = self.repository.create_user(user_data)

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya existe",
                )

            return {"message": "El usuario fue registrado exitosamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def get_all_persons(self, page: int, per_page: int):
        try:
            skip = (page - 1) * per_page

            # Get counts
            total_vigilantes = self.repository.get_vigilantes_count()
            total_aprendices = self.repository.get_aprendices_count()
            total_admins = self.repository.get_admins_count()

            # Get paginated data
            vigilants = self.repository.get_vigilantes_paginated(skip, per_page)
            aprendices = self.repository.get_aprendices_paginated(skip, per_page)
            admins = self.repository.get_admins_paginated(skip, per_page)

            # Add roll information
            vigilantes_with_roll = [{'roll': 'vigilante', **vigilante.__dict__} for vigilante in vigilants]
            aprendices_with_roll = [{'roll': 'aprendiz', **aprendiz.__dict__} for aprendiz in aprendices]
            admins_with_roll = [{'roll': 'admin', **admin.__dict__} for admin in admins]

            # Combine results
            unidos = vigilantes_with_roll + aprendices_with_roll + admins_with_roll
            total_items = total_vigilantes + total_aprendices + total_admins

            return {
                "total_items": total_items,
                "page": page,
                "per_page": per_page,
                "items": unidos
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def edit_user_by_person(self, document: int, roll: int):
        try:
            if roll not in [1, 2, 3]:
                raise HTTPException(status_code=400, detail="Rol no válido")

            user = self.repository.get_user_by_document_and_roll(document, roll)

            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            return "Usuario actualizado exitosamente"
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
