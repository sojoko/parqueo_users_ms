from fastapi import HTTPException
from config.database import Session
from models.vigilantes import Vigilantes as VigilanteModel
from schemas.vigilantes import Vigilantes, ChangeStatusRequest

class VigilanteService:
    def create_vigilante(self, vigilantes: Vigilantes):
        db = Session()
        try:   
            vigilantes.document = int(vigilantes.document)
            existing_vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == vigilantes.document).first()
            if existing_vigilante:
                raise HTTPException(status_code=400, detail="El documento ya está registrado")
            new_vigilante = VigilanteModel(
                name=vigilantes.name,
                last_name=vigilantes.last_name,
                document=vigilantes.document
            )
            db.add(new_vigilante)
            db.commit()

            return {"message": "El usuario vigilante fue registrado correctamente"}

        except ValueError as ve:     
            raise HTTPException(status_code=400, detail=f"Error de validación: {str(ve)}")    
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()

    def update_vigilante(self, document: int, vigilantes: Vigilantes):
        db = Session()
        try:
            vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()

            if not vigilante:
                raise HTTPException(status_code=404, detail="Vigilante no encontrado")

            vigilante.name = vigilantes.name
            vigilante.last_name = vigilantes.last_name
            vigilante.document = int(vigilantes.document)

            db.commit()

            return {"message": "El usuario vigilante fue actualizado correctamente"}
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def get_vigilante_by_id(self, id: int):
        db = Session()
        try:
            vigilante = db.query(VigilanteModel).filter(VigilanteModel.id == id).first()

            if not vigilante:
                raise HTTPException(status_code=404, detail="Vigilante no encontrado")

            user_dict = vigilante.__dict__
            user_dict['role_id'] = 3

            return user_dict
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def get_vigilante_by_document(self, document: int):
        db = Session()
        try:
            vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()

            if not vigilante:
                raise HTTPException(status_code=404, detail="Vigilante no encontrado")

            user_dict = vigilante.__dict__
            user_dict['roll'] = "vigilante"

            return user_dict
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def get_all_vigilant(self, page: int, per_page: int):
        try:
            db = Session()
            try:
                skip = (page - 1) * per_page
                vigilants = db.query(VigilanteModel).offset(skip).limit(per_page).all()
                vigilantes_with_roll = []
                for vigilante in vigilants:
                    user_dict = vigilante.__dict__
                    user_dict['roll'] = "vigilante"
                    vigilantes_with_roll.append(user_dict)
                return vigilantes_with_roll
            finally:
                db.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")

    def change_vigilante_status(self, req: ChangeStatusRequest):
        try:
            vigilante_id = int(req.id)
            status_id = int(req.status_id)

            db = Session()
            try:
                vigilante = db.query(VigilanteModel).filter(VigilanteModel.id == vigilante_id).first()

                if not vigilante:
                    raise HTTPException(status_code=404, detail="El vigilante no fue encontrado")

                vigilante.status = status_id
                db.commit()

                return {"message": "El estado del vigilante fue actualizado correctamente"}
            except HTTPException as http_exc:
                db.rollback()
                raise http_exc
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
            finally:
                db.close()
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
