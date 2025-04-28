from fastapi import APIRouter, Depends, HTTPException, Query, Request
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from models.vigilantes import Vigilantes as VigilanteModel
from schemas.vigilantes import Vigilantes

    
vigilante_router = APIRouter()

@limiter.limit("20/minute")
@vigilante_router.post("/api/v1/vigilantes-registration", tags=['Vigilantes'])
async def create_vigilante(request:Request, vigilantes: Vigilantes, token: TokenData = Depends(verify_token)):
    db = Session()
    try:   
        vigilantes.document = int(vigilantes.document)
        existing_vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == vigilantes.document).first()
        if existing_vigilante:
            raise HTTPException(status_code=400, detail="El documento ya está registrado")
        new_vigilante = VigilanteModel(
            name=vigilantes.name,
            last_name=vigilantes.last_name,
            document=vigilantes.document
        )
        db.add(new_vigilante)
        db.commit()
        
        return {"message": "El usuario vigilante fue registrado correctamente"}
    
    except ValueError as ve:     
        raise HTTPException(status_code=400, detail=f"Error de validación: {str(ve)}")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close() 
@limiter.limit("20/minute")
@vigilante_router.put("/api/v1/vigilantes-update/{document}", tags=['Vigilantes'])
async def update_vigilante(request:Request, document: int, vigilantes: Vigilantes, token: TokenData = Depends(verify_token)):
    db = Session()
    try:
        vigilante = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()
        
        if not vigilante:
            raise HTTPException(status_code=404, detail="Vigilante no encontrado")
        
        vigilante.name = vigilantes.name
        vigilante.last_name = vigilantes.last_name
        vigilante.document = int(vigilantes.document)
        
        db.commit()
        
        return {"message": "El usuario vigilante fue actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()

@limiter.limit("20/minute")
@vigilante_router.get("/api/v1/vigilantes-all", tags=['Vigilantes'])
async def get_all_vigilant(request:Request, page: int = Query(1, ge=1), per_page: int = Query(5, ge=1), token: TokenData = Depends(verify_token)):
    try:
        db = Session()
        try:
            skip = (page - 1) * per_page
            vigilants = db.query(VigilanteModel).offset(skip).limit(per_page).all()
            vigilantes_with_roll = []
            for vigilante in vigilants:
                user_dict = vigilante.__dict__
                user_dict['roll'] = "vigilante"
                vigilantes_with_roll.append(user_dict)
            return JSONResponse(status_code=200, content=jsonable_encoder(vigilantes_with_roll))
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()


