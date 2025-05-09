from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from schemas.vehicles import Motocicletas
from schemas.vehicles import Bicicleta
from services.vehicles_service import VehiclesService

vehicle_router = APIRouter()
vehicles_service = VehiclesService()

@limiter.limit("10/day")
@limiter.limit("5/hour")
@vehicle_router.post("/api/v1/motocicleta-registration", tags=['Vehiculos'])
async def create_moto(request:Request, motocicletas: Motocicletas):
    result = vehicles_service.create_moto(motocicletas)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("10/day")
@limiter.limit("5/hour")
@vehicle_router.post("/api/v1/bicicleta-registration", tags=['Vehiculos'])
async def create_byci(request:Request, bicicleta: Bicicleta):
    result = vehicles_service.create_byci(bicicleta)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("30/minute")
@vehicle_router.get("/api/v1/moto/{document}", tags=['Vehiculos'])
def get_moto_by_user_document(request:Request, document: int, token: TokenData = Depends(verify_token)):
    moto = vehicles_service.get_moto_by_user_document(document)
    return JSONResponse(status_code=200, content=jsonable_encoder(moto))

@limiter.limit("30/minute")
@vehicle_router.get("/api/v1/vehicle/{document}", tags=['Vehiculos'])
def get_vehicle_by_user_document(request:Request, document: int, token: TokenData = Depends(verify_token)):
    vehicles = vehicles_service.get_vehicle_by_user_document(document)
    return JSONResponse(status_code=200, content=jsonable_encoder(vehicles))
