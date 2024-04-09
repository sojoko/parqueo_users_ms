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



vehicle_router = APIRouter()


@vehicle_router.post("/api/v1/motocicleta-registration", tags=['Vehiculos'])
async def create_moto(motocicletas: Motocicletas):
    try:
        
        foto_default = "https://es.wikipedia.org/wiki/Motocicleta#/media/Archivo:Ducati_748_Studio.jpg"
        soat_default = "https://live.staticflickr.com/3905/14932621607_964758d36e_b.jpg"
        tarjeta_propiedad_default = "https://live.staticflickr.com/5595/15118817242_45e787b25e_b.jpg"       
        motocicletas.user_document = int(motocicletas.user_document)        
        db = Session()
        new_moto = MotoModel(
            user_document = motocicletas.user_document,
            placa = motocicletas.placa,
            marca = motocicletas.marca,
            modelo = motocicletas.modelo,
            color = motocicletas.color,
            foto = foto_default,
            soat = soat_default,
            tarjeta_propiedad = tarjeta_propiedad_default,
            observaciones = motocicletas.observaciones,    
        )
        db.add(new_moto)
        db.commit()
        return {"message": "La motocicleta fue registrada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")


@vehicle_router.get("/api/v1/aprendices/id/document/{id}", tags=['Aprendices'])
def get_aprendiz_by_id(id: int):
    db = Session()
    aprendiz_by_id = db.query(AprendizModel).filter(AprendizModel.id == id).first()
    return JSONResponse(status_code=200, content=jsonable_encoder(aprendiz_by_id))


@vehicle_router.get("/api/v1/moto/{document}", tags=['Vehiculos'])
def get_moto_by_user_document(document: int):
    db = Session()
    moto_by_user_document = db.query(MotoModel).filter(MotoModel.user_document == document).first()
    if moto_by_user_document is None:
        raise HTTPException(status_code=404, detail="El vehiculo no fue encontrado")   
    return JSONResponse(status_code=200, content=jsonable_encoder(moto_by_user_document))


@vehicle_router.get("/api/v1/aprendiz-status/{document}", tags=['Estatus de Aprendices'])
def get_aprendiz_satus(document: int):
    db = Session()
    aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()
    if aprendiz is None:
        raise HTTPException(status_code=404, detail="El documento no fue encontrado")   
    
    aprendiz_status_id = db.query(AprendizModel).filter(AprendizModel.document == document).first().state_id
    status = db.query(EstadoAprendiz).filter(EstadoAprendiz.id == aprendiz_status_id).first().estado
    return JSONResponse(status_code=200, content=jsonable_encoder(status))