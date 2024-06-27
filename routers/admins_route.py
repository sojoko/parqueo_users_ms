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


@admins_router.get("/api/v1/admins-all", tags=['admins'])
async def get_all_admins():
    try:      
        db = Session()  
        admins = db.query(AdminModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(admins))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")



@admins_router.put("/api/v1/admins-update/{document}", tags=['admins'])
async def update_admin(document: int, admins: Admins):
    db = Session()
    try:
        # Buscar el administrador por el documento
        admin = db.query(AdminModel).filter(AdminModel.document == document).first()
        
        if not admin:
            raise HTTPException(status_code=404, detail="Administrador no encontrado")
        
        # Actualizar los datos del administrador
        admin.name = admins.name if admins.name else admin.name
        admin.last_name = admins.last_name if admins.last_name else admin.last_name
        admin.document = int(admins.document) if admins.document else admin.document
        
        db.commit()
        
        return {"message": "El usuario administrador fue actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")