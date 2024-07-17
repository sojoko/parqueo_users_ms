from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from models.aprendices import Aprendices as AprendizModel
from schemas.aprendices import Aprendices
from models.aprendices import EstadoAprendiz
from models.vehicles import Motocicleta as MotoModel
from schemas.vehicles import Motocicletas
from models.vehicles import Bicicleta as BiciModel
from schemas.vehicles import Bicicleta



vehicle_router = APIRouter()


@vehicle_router.post("/api/v1/motocicleta-registration", tags=['Vehiculos'])
async def create_moto(motocicletas: Motocicletas):
    try:            
        motocicletas.user_document = int(motocicletas.user_document)   
        vehicle_type = 1   
        db = Session()
        new_moto = MotoModel(
            vehicle_type = vehicle_type,
            user_document = motocicletas.user_document,
            placa = motocicletas.placa,
            marca = motocicletas.marca,
            modelo = motocicletas.modelo,
            color = motocicletas.color,
            foto = motocicletas.foto,         
            tarjeta_propiedad = motocicletas.tarjeta_propiedad,
            observaciones = motocicletas.observaciones,    
        )
        db.add(new_moto)
        db.commit()
        return {"message": "La motocicleta fue registrada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    
    
@vehicle_router.post("/api/v1/bicicleta-registration", tags=['Vehiculos'])
async def create_byci(bicicleta: Bicicleta):
    try:            
        bicicleta.user_document = int(bicicleta.user_document)   
        vehicle_type = 2  
        db = Session()
        new_moto = BiciModel(
            vehicle_type = vehicle_type,
            user_document = bicicleta.user_document,
            numero_marco = bicicleta.numero_marco,
            marca = bicicleta.marca,
            modelo = bicicleta.modelo,
            color = bicicleta.color,
            foto = bicicleta.foto,         
            tarjeta_propiedad = bicicleta.tarjeta_propiedad,
            observaciones = bicicleta.observaciones,    
        )
        db.add(new_moto)
        db.commit()
        return {"message": "La bicileta fue registrada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")


@vehicle_router.get("/api/v1/moto/{document}", tags=['Vehiculos'])
def get_moto_by_user_document(document: int):
    db = Session()
    moto_by_user_document = db.query(MotoModel).filter(MotoModel.user_document == document).first()
    if moto_by_user_document is None:
        raise HTTPException(status_code=404, detail="El vehiculo no fue encontrado")   
    return JSONResponse(status_code=200, content=jsonable_encoder(moto_by_user_document))


@vehicle_router.get("/api/v1/vehicle/{document}", tags=['Vehiculos'])
def get_vehicle_by_user_document(document: int):
    db = Session()
    moto_by_user_document = db.query(MotoModel).filter(MotoModel.user_document == document).first()
    bici_by_user_document = db.query(MotoModel).filter(MotoModel.user_document == document).first()
    vehicle_for_sent = []
    if moto_by_user_document is not None:
        vehicle_for_sent = moto_by_user_document
    if bici_by_user_document is not None:
        vehicle_for_sent = bici_by_user_document
    
    if moto_by_user_document is None:
        raise HTTPException(status_code=404, detail="El vehiculo no fue encontrado")   
    return JSONResponse(status_code=200, content=jsonable_encoder(vehicle_for_sent))
