from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from models.aprendices import Aprendices as AprendizModel
from schemas.aprendices import Aprendices, ChangeStatusRequest
from models.aprendices import EstadoAprendiz
from models.vehicles import Motocicleta as MotocicletaModel
from models.vehicles import Bicicleta as BicicletaModel
from typing import List, Optional

aprendices_router = APIRouter()

@aprendices_router.get("/api/v1/aprendices-all", tags=['Aprendices'])
def get_user_all(token: TokenData = Depends(verify_token)):
    db = Session()  
    aprendinces = db.query(AprendizModel).all()
    aprendices_with_roll = []
    for user in aprendinces:
        user_dict = user.__dict__
        user_dict['roll'] = "aprendiz"
        aprendices_with_roll.append(user_dict)
    db.close() 
    return JSONResponse(status_code=200, content=jsonable_encoder(aprendices_with_roll))   
    


@aprendices_router.post("/api/v1/aprendiz-registration", tags=['Aprendices'])
async def create_aprendiz(aprendices: Aprendices, token: TokenData = Depends(verify_token)):
    
    db = Session()
    aprendiz_exist = db.query(AprendizModel).filter(AprendizModel.document == aprendices.document).first()
    if aprendiz_exist:
            raise HTTPException(status_code=400, detail="El documento ya existe") 
    try:
        finish_date = datetime.strptime(aprendices.finish_date, "%Y-%m-%d")        
        status_default = 1
        aprendices.document = int(aprendices.document)
        aprendices.ficha = int(aprendices.ficha)           
        new_aprendiz = AprendizModel(
            name=aprendices.name,
            last_name=aprendices.last_name,
            document=aprendices.document,
            ficha=aprendices.ficha,
            photo=aprendices.photo,
            email=aprendices.email,     
            finish_date=finish_date,
            state_id=status_default
        )
        db.add(new_aprendiz)
        db.commit()
        return {"message": "El aprendiz fue registrado exitosamente"}
    except Exception:
        raise HTTPException(status_code=500, detail=f"Error en la operación")
    finally:
        db.close()  


@aprendices_router.get("/api/v1/aprendices/id/document/{id}", tags=['Aprendices'])
def get_aprendiz_by_id(id: int, token: TokenData = Depends(verify_token)):
    db = Session()
    try:      
        aprendiz_by_id = db.query(AprendizModel).filter(AprendizModel.id == id).first()       
        if aprendiz_by_id is None:
            raise HTTPException(status_code=404, detail="El aprendiz no fue encontrado")        
        return JSONResponse(status_code=200, content=jsonable_encoder(aprendiz_by_id))    
    except HTTPException as http_exc:      
        raise http_exc
    except Exception as e:        
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close()  


@aprendices_router.get("/api/v1/aprendices/{document}", tags=['Aprendices'])
def get_aprendiz_by_document(document: int, token: TokenData = Depends(verify_token)):
    db = Session()
    try:
        aprendiz_by_document = db.query(AprendizModel).filter(AprendizModel.document == document).first()
        if aprendiz_by_document is None:
            raise HTTPException(status_code=404, detail="El documento no fue encontrado")
        return JSONResponse(status_code=200, content=jsonable_encoder(aprendiz_by_document))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()


@aprendices_router.get("/api/v1/aprendiz-status/{document}", tags=['Aprendices'])
def get_aprendiz_status_by_document(document: int):
    db = Session()
    try:
        aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()
        
        if aprendiz is None:
            raise HTTPException(status_code=404, detail="El documento no fue encontrado")
        aprendiz_status_id = aprendiz.state_id 
        status = db.query(EstadoAprendiz).filter(EstadoAprendiz.id == aprendiz_status_id).first()        
        if status is None:
            raise HTTPException(status_code=404, detail="Estado del aprendiz no encontrado")        
        return JSONResponse(status_code=200, content=jsonable_encoder(status.estado))
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:     
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close() 



@aprendices_router.get("/api/v1/aprendiz-status", tags=['Estatus de Aprendices'])
def get_aprendiz_status(
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1),
    token: TokenData = Depends(verify_token)
):
    db = Session()
    aprendices = db.query(AprendizModel).all()
    motocicletas = db.query(MotocicletaModel).all()
    bicicletas = db.query(BicicletaModel).all()
    
    aprendices_dict = {aprendiz.document: aprendiz for aprendiz in aprendices}
    
    for motocicleta in motocicletas:
        if motocicleta.user_document in aprendices_dict:
            aprendiz = aprendices_dict[motocicleta.user_document]
            aprendiz.vehicle = motocicleta
    
    for bicicleta in bicicletas:
        if bicicleta.user_document in aprendices_dict:
            aprendiz = aprendices_dict[bicicleta.user_document]
            aprendiz.vehicle = bicicleta
    
    aprendices_combined = list(aprendices_dict.values())
    total_items = len(aprendices_combined)
    start = (page - 1) * per_page
    end = start + per_page
    aprendices_paginated = aprendices_combined[start:end]
    
    if not aprendices_paginated:
        raise HTTPException(status_code=404, detail="No hay aprendices en esta página")

    return JSONResponse(
        status_code=200,
        content={
            "total_items": total_items,
            "page": page,
            "per_page": per_page,
            "items": jsonable_encoder(aprendices_paginated)
        }
    )
    

@aprendices_router.get("/api/v1/aprendiz-statu/{document}", tags=['Aprendices'])
def get_aprendiz_status(document: int, token: TokenData = Depends(verify_token)):
    db = Session()
    try:
        aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()    
        vehicles = db.query(MotocicletaModel).filter(MotocicletaModel.user_document == document).all()
        
        aprendiz_dict = jsonable_encoder(aprendiz) if aprendiz else {}
        vehicles_list = jsonable_encoder(vehicles) if vehicles else []
        
        vehicles_dict = {"vehicle_" + str(i): vehicle for i, vehicle in enumerate(vehicles_list)}
        
        response_data = {**aprendiz_dict, **vehicles_dict}
        
        return JSONResponse(status_code=200, content=response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close() 


@aprendices_router.put("/api/v1/aprendiz-change-status", tags=['Aprendices'])
def change_aprendiz_status(req: ChangeStatusRequest, token: TokenData = Depends(verify_token)):
    db = Session()
    try:
        document = int(req.document)        
        aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()
        
        if aprendiz is None:
            raise HTTPException(status_code=404, detail="El documento no fue encontrado")
        
        aprendiz.state_id = int(req.state_id)
        db.commit()
        
        return JSONResponse(status_code=200, content=jsonable_encoder({"message": "El estado del aprendiz fue actualizado correctamente"}))
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close()  


@aprendices_router.put("/api/v1/aprendiz-update/{document}", tags=['Aprendices'])
async def update_aprendiz(document: int, aprendices: Aprendices, token: TokenData = Depends(verify_token)):
    db = Session()
    try:
        aprendiz = db.query(AprendizModel).filter(AprendizModel.document == document).first()        
        if not aprendiz:
            raise HTTPException(status_code=404, detail="Aprendiz no encontrado")
        aprendiz.name = aprendices.name if aprendices.name else aprendiz.name
        aprendiz.last_name = aprendices.last_name if aprendices.last_name else aprendiz.last_name
        aprendiz.document = int(aprendices.document) if aprendices.document else aprendiz.document
        aprendiz.ficha = int(aprendices.ficha) if aprendices.ficha else aprendiz.ficha
        aprendiz.email = aprendices.email if aprendices.email else aprendiz.email       
        db.commit()
        
        return {"message": "El aprendiz fue actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()  
