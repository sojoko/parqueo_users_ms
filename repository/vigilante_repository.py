from fastapi import HTTPException
from config.database import Session
from models.vigilantes import Vigilantes as VigilanteModel
from schemas.vigilantes import Vigilantes, ChangeStatusRequest

class VigilanteRepository:
    def create_vigilante(self, vigilantes):
        db = Session()
        try:
            vigilantes.document = int(vigilantes.document)
            existing_vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == vigilantes.document).first()

            if existing_vigilante:
                return False

            new_vigilante = VigilanteModel(
                name=vigilantes.name,
                last_name=vigilantes.last_name,
                document=vigilantes.document
            )
            db.add(new_vigilante)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def update_vigilante(self, document, vigilantes):
        db = Session()
        try:
            vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()

            if not vigilante:
                return None

            vigilante.name = vigilantes.name
            vigilante.last_name = vigilantes.last_name
            vigilante.document = int(vigilantes.document)

            db.commit()
            return vigilante
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def get_vigilante_by_id(self, id):
        db = Session()
        try:
            vigilante = db.query(VigilanteModel).filter(VigilanteModel.id == id).first()
            if not vigilante:
                return None

            return {
                'id': vigilante.id,
                'name': vigilante.name,
                'last_name': vigilante.last_name,
                'document': vigilante.document,
                'registry_date': vigilante.registry_date,
                'status_id': vigilante.status_id,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def get_vigilante_by_document(self, document):
        db = Session()
        try:
            vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()
            if not vigilante:
                return None

            return {
                'id': vigilante.id,
                'name': vigilante.name,
                'last_name': vigilante.last_name,
                'document': vigilante.document,
                'registry_date': vigilante.registry_date,
                'status_id': vigilante.status_id,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def get_all_vigilant(self, skip, limit):
        db = Session()
        try:
            vigilantes = db.query(VigilanteModel).offset(skip).limit(limit).all()
            return [
                {
                    'id': v.id,
                    'name': v.name,
                    'last_name': v.last_name,
                    'document': v.document,
                    'registry_date': v.registry_date,
                    'status_id': v.status_id,
                }
                for v in vigilantes
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()

    def change_vigilante_status(self, request):
        db = Session()
        try:
            vigilante_id = int(request.id)
            status_id = int(request.status_id)

            vigilante = db.query(VigilanteModel).filter(VigilanteModel.id == vigilante_id).first()

            if not vigilante:
                return None

            vigilante.status_id = status_id
            db.commit()
            return vigilante
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
