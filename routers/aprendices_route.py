from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from models.aprendices import Aprendices as AprendizModel
from schemas.aprendices import Aprendices
from models.aprendices import EstadoAprendiz



aprendices_router = APIRouter()


@aprendices_router.post("/api/v1/aprendiz-registration", tags=['Aprendices'])
async def create_aprendiz(aprendices: Aprendices):
    try:
        finish_date = datetime.strptime(aprendices.finish_date, "%Y-%m-%d")
        photo_default = "https://live.staticflickr.com/2753/4374393040_17f13bcc4b_b.jpg"
        status_default = 1
        aprendices.document = int(aprendices.document)
        aprendices.ficha = int(aprendices.ficha)
        db = Session()
        new_aprendiz = AprendizModel(
            name=aprendices.name,
            last_name=aprendices.last_name,
            document=aprendices.document,
            ficha=aprendices.ficha,
            photo=photo_default,  
            email=aprendices.email,     
            finish_date=finish_date,
            state_id=status_default
            
        )
        db.add(new_aprendiz)
        db.commit()
        return {"message": "El aprendiz fue registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")


@aprendices_router.get("/api/v1/aprendices/id/document/{id}", tags=['Aprendices'])
def get_aprendiz_by_id(id: int):
    db = Session()
    aprendiz_by_id = db.query(AprendizModel).filter(AprendizModel.id == id).first()
    return JSONResponse(status_code=200, content=jsonable_encoder(aprendiz_by_id))


@aprendices_router.get("/api/v1/aprendices/{document}", tags=['Aprendices'])
def get_aprendiz_by_document(document: int):
    db = Session()
    aprendiz_by_document = db.query(AprendizModel).filter(AprendizModel.document == document).first()
    if aprendiz_by_document is None:
        raise HTTPException(status_code=404, detail="El documento no fue encontrado")   
    return JSONResponse(status_code=200, content=jsonable_encoder(aprendiz_by_document))


@aprendices_router.get("/api/v1/aprendiz-status/{document}", tags=['Estatus de Aprendices'])
def get_aprendiz_satus(document: int):
    db = Session()
    aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()
    if aprendiz is None:
        raise HTTPException(status_code=404, detail="El documento no fue encontrado")   
    
    aprendiz_status_id = db.query(AprendizModel).filter(AprendizModel.document == document).first().state_id
    status = db.query(EstadoAprendiz).filter(EstadoAprendiz.id == aprendiz_status_id).first().estado
    return JSONResponse(status_code=200, content=jsonable_encoder(status))