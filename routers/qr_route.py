from fastapi import APIRouter, HTTPException
from models.qr import QR as QRModel
from schemas.qr import QR 
from qr import qr_generator
from base64 import b64encode, b64decode
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

qr_router = APIRouter()


@qr_router.post("/api/v1/qr", tags=['QR'])
def create_qr(qr: QR, document: int):
    db = Session()
    document = int(document)   
    
    try_to_exist_qr = db.query(QRModel).filter(QRModel.user_document == document).first()
    
    if try_to_exist_qr:
        last_qr_date = db.query(QRModel).filter(QRModel.user_document == document).order_by(QRModel.registry_date.desc()).first().registry_date
        last_qr_image = db.query(QRModel).filter(QRModel.user_document == document).order_by(QRModel.registry_date.desc()).first().qr_image
        fecha_actual = datetime.now()
        time_limit = timedelta(hours=1)
        diferencia = fecha_actual - last_qr_date
        last_qr_image_decode = b64encode(last_qr_image).decode('utf-8')

        if diferencia < time_limit:
            return JSONResponse(status_code=200, content=jsonable_encoder(last_qr_image_decode))
    
    
    date_request = f'/api/v1/aprendices/{document}'
    qr_binary = b64decode(qr_generator(date_request=date_request))
    qr.qr = qr_binary
    qr.user_document = document
    
    new_qr = QRModel(
            qr_image = qr.qr,
            user_document=qr.user_document,             
        )
    db.add(new_qr)
    db.commit()
    
    qr_code_generated = db.query(QRModel).filter(QRModel.user_document == document).order_by(QRModel.registry_date.desc()).first().qr_image
    qr_code_generated_binary = b64encode(qr_code_generated).decode('utf-8')
    
    return JSONResponse(status_code=200, content=jsonable_encoder(qr_code_generated_binary))