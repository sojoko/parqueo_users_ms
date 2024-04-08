from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from models.vigilantes import Vigilantes as VigilanteModel
from schemas.vigilantes import Vigilantes
from models.aprendices import EstadoAprendiz



vigilante_router = APIRouter()


@vigilante_router.post("/api/v1/vigilantes-registration", tags=['Vigilantes'])
async def create_vigilante(vigilantes: Vigilantes):
    db = Session()
    try:       
     
        vigilantes.document = int(vigilantes.document)
        db = Session()
        new_vigitalente = VigilanteModel(
            name=vigilantes.name,
            last_name=vigilantes.last_name,
            document=vigilantes.document          
                          
        )
        db.add(new_vigitalente)
        db.commit()
        return {"message": "El usuario vigilante fue regitrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")


