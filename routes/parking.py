from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from schemas.parking import Parking
from fastapi import Depends, HTTPException, status
from fastapi import Request
from services.parking_service import ParkingService


parking_router = APIRouter()
parking_service = ParkingService()

@limiter.limit("20/day")
@limiter.limit("10/hour")
@parking_router.post("/api/v1/parking-registration", tags=['parking'])
async def create_parking(request:Request, parking : Parking, token: TokenData = Depends(verify_token)):
    result = parking_service.create_parking(parking)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("30/minute")
@parking_router.get("/api/v1/parking-all", tags=['parking'])
async def get_all_parking(request:Request, token: TokenData = Depends(verify_token)):
    parking = parking_service.get_all_parking()
    return JSONResponse(status_code=200, content=jsonable_encoder(parking))

@limiter.limit("30/minute")
@parking_router.get("/api/v1/parking-all-counter", tags=['parking'])
async def get_all_parking_counter(request:Request, token: TokenData = Depends(verify_token)):
    response = parking_service.get_all_parking_counter()
    return JSONResponse(status_code=200, content=jsonable_encoder(response))

@limiter.limit("30/minute")
@parking_router.get("/api/v1/parking-by-document/{user_document}", tags=['parking'])
async def get_parking_by_document(request:Request, user_document: int, token: TokenData = Depends(verify_token)):
    parking = parking_service.get_parking_by_document(user_document)
    return JSONResponse(status_code=200, content=jsonable_encoder(parking))

@limiter.limit("20/minute")
@parking_router.put("/api/v1/parking-registration-update/{user_document}", tags=['parking'])
async def update_parking(request:Request, user_document: int, parking: Parking, token: TokenData = Depends(verify_token)):
    result = parking_service.update_parking(user_document, parking)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
