from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from schemas.admins import Admins, ChangeStatusRequest
from services.admins_service import AdminsService


admins_router = APIRouter()
admins_service = AdminsService()


@limiter.limit("10/day")
@limiter.limit("5/hour")
@admins_router.post("/api/v1/admins-registration", tags=['admins'])
async def create_admin(request: Request, admins : Admins, token: TokenData = Depends(verify_token)):
    result = admins_service.create_admin(admins)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@admins_router.get("/api/v1/admins-all", tags=['admins'])
async def get_all_admins(request: Request, token: TokenData = Depends(verify_token)):
    admins = admins_service.get_all_admins()
    return JSONResponse(status_code=200, content=jsonable_encoder(admins))


@limiter.limit("20/minute")
@admins_router.put("/api/v1/admins-update/{document}", tags=['admins'])
async def update_admin(request: Request, document: int, admins: Admins, token: TokenData = Depends(verify_token)):
    result = admins_service.update_admin(document, admins)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@admins_router.get("/api/v1/admin-by-id/{id}", tags=['admins'])
async def get_admin_by_id(request: Request, id: int, token: TokenData = Depends(verify_token)):
    admin = admins_service.get_admin_by_id(id)
    return JSONResponse(status_code=200, content=jsonable_encoder(admin))

@limiter.limit("20/minute")
@admins_router.put("/api/v1/admin-change-status", tags=['admins'])
async def change_admin_status(request: Request, req: ChangeStatusRequest, token: TokenData = Depends(verify_token)):
    result = admins_service.change_admin_status(req)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
