from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from schemas.vigilantes import Vigilantes, ChangeStatusRequest
from services.vigilante_service import VigilanteService

vigilante_router = APIRouter()
vigilante_service = VigilanteService()

@limiter.limit("20/minute")
@vigilante_router.post("/api/v1/vigilantes-registration", tags=['Vigilantes'])
async def create_vigilante(request:Request, vigilantes: Vigilantes, token: TokenData = Depends(verify_token)):
    result = vigilante_service.create_vigilante(vigilantes)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@vigilante_router.put("/api/v1/vigilantes-update/{document}", tags=['Vigilantes'])
async def update_vigilante(request:Request, document: int, vigilantes: Vigilantes, token: TokenData = Depends(verify_token)):
    result = vigilante_service.update_vigilante(document, vigilantes)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@vigilante_router.get("/api/v1/vigilantes-all", tags=['Vigilantes'])
async def get_all_vigilant(request:Request, page: int = Query(1, ge=1), per_page: int = Query(5, ge=1), token: TokenData = Depends(verify_token)):
    vigilantes = vigilante_service.get_all_vigilant(page, per_page)
    return JSONResponse(status_code=200, content=jsonable_encoder(vigilantes))

@limiter.limit("20/minute")
@vigilante_router.get("/api/v1/vigilante/{document}", tags=['Vigilantes'])
async def get_vigilante_by_document(request: Request, document: int, token: TokenData = Depends(verify_token)):
    vigilante = vigilante_service.get_vigilante_by_document(document)
    return JSONResponse(status_code=200, content=jsonable_encoder(vigilante))

@limiter.limit("20/minute")
@vigilante_router.get("/api/v1/vigilante-by-id/{id}", tags=['Vigilantes'])
async def get_vigilante_by_id(request: Request, id: int, token: TokenData = Depends(verify_token)):
    vigilante = vigilante_service.get_vigilante_by_id(id)
    return JSONResponse(status_code=200, content=jsonable_encoder(vigilante))

@limiter.limit("20/minute")
@vigilante_router.put("/api/v1/vigilante-change-status", tags=['Vigilantes'])
async def change_vigilante_status(request: Request, req: ChangeStatusRequest, token: TokenData = Depends(verify_token)):
    result = vigilante_service.change_vigilante_status(req)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
