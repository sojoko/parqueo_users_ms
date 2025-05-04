from fastapi import HTTPException
from config.database import Session
from models.admins import Admins as AdminModel

class AdminRepository:
    def create_admin(self, admin_data: dict):
        db = Session()
        try:
            admin_exist = db.query(AdminModel).filter(AdminModel.document == admin_data["document"]).first()
            if admin_exist:
                return False

            new_admin = AdminModel(**admin_data)
            db.add(new_admin)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def get_all_admins(self):
        db = Session()
        try:
            admins = db.query(AdminModel).all()
            return admins
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()
    
    def update_admin(self, document: int, admin_data: dict):
        db = Session()
        try:
            admin = db.query(AdminModel).filter(AdminModel.document == document).first()
            if not admin:
                return False

            for key, value in admin_data.items():
                setattr(admin, key, value)
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
        finally:
            db.close()