from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from models.admins import Admins as AdminModel
from schemas.admins import Admins
from fastapi import Depends, HTTPException, status




admins_router = APIRouter()


@admins_router.post("/api/v1/admins-registration", tags=['admins'])
async def create_admin(admins : Admins):
    db = Session()
    admins.document = int(admins.document)
    
    user_exist = db.query(AdminModel).filter(AdminModel.document == admins.document).first()
    if user_exist:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
            )
    try:      
     
        
        new_admin = AdminModel(
            name=admins.name,
            last_name=admins.last_name,
            document=admins.document          
                          
        )
        db.add(new_admin)
        db.commit()
        return {"message": "El usuario Admin fue regitrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")


