from fastapi import HTTPException, status
from config.database import Session
from models.users import User as UserModel
from models.aprendices import Aprendices as AprendizModel
from models.vigilantes import Vigilantes as VigilanteModel
from models.admins import Admins as AdminModel
from schemas.usersRegistry import UserRegistry

class UserRepository:
    def get_user_by_document(self, document: int):
        db = Session()
        try:
            user = db.query(UserModel).filter(UserModel.document == document).first()        
            return user    
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def delete_user_by_document_and_roll(self, document: int, roll: int):
        db = Session()
        try:
            user = None
            if roll == 1:
                user = db.query(AdminModel).filter(AdminModel.document == document).first()
            elif roll == 2:
                user = db.query(AprendizModel).filter(AprendizModel.document == document).first()
            elif roll == 3:
                user = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()
            
            if user is not None:
                db.delete(user)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_all_users(self):
        db = Session()
        try:
            users = db.query(UserModel).all()        
            return users
        except Exception as e:     
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def get_user_by_document_with_password(self, document: int):
        db = Session()
        try:
            user = db.query(UserModel).filter(UserModel.document == document).first()
            return user
        except Exception as e:       
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def get_admin_name_by_document(self, document: int):
        db = Session()
        try:
            admin = db.query(AdminModel).filter(AdminModel.document == document).first()
            return admin.name if admin else None
        except Exception as e:       
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def get_aprendiz_name_by_document(self, document: int):
        db = Session()
        try:
            aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()
            return aprendiz.name if aprendiz else None
        except Exception as e:       
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def get_vigilante_name_by_document(self, document: int):
        db = Session()
        try:
            vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()
            return vigilante.name if vigilante else None
        except Exception as e:       
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
        finally:
            db.close()
    
    def create_user(self, user_data: dict):
        db = Session()
        try:
            user_exist = db.query(UserModel).filter(UserModel.document == user_data["document"]).first()
            if user_exist:
                return False
                
            new_user = UserModel(**user_data)
            db.add(new_user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_vigilantes_count(self):
        db = Session()
        try:
            count = db.query(VigilanteModel).count()
            return count
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_aprendices_count(self):
        db = Session()
        try:
            count = db.query(AprendizModel).count()
            return count
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_admins_count(self):
        db = Session()
        try:
            count = db.query(AdminModel).count()
            return count
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_vigilantes_paginated(self, skip: int, limit: int):
        db = Session()
        try:
            vigilantes = db.query(VigilanteModel).offset(skip).limit(limit).all()
            return vigilantes
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_aprendices_paginated(self, skip: int, limit: int):
        db = Session()
        try:
            aprendices = db.query(AprendizModel).offset(skip).limit(limit).all()
            return aprendices
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_admins_paginated(self, skip: int, limit: int):
        db = Session()
        try:
            admins = db.query(AdminModel).offset(skip).limit(limit).all()
            return admins
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_user_by_document_and_roll(self, document: int, roll: int):
        db = Session()
        try:
            user = None
            if roll == 1:
                user = db.query(AdminModel).filter(AdminModel.document == document).first()
            elif roll == 2:
                user = db.query(AprendizModel).filter(AprendizModel.document == document).first()
            elif roll == 3:
                user = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()
            
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()