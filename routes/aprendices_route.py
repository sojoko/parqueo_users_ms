from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from schemas.aprendices import Aprendices, ChangeStatusRequest
from fastapi import Request
from services.aprendices_service import AprendicesService

aprendices_router = APIRouter()
aprendices_service = AprendicesService()

@limiter.limit("20/minute")
@aprendices_router.get("/api/v1/aprendices-all", tags=['Aprendices'])
def get_user_all(request: Request, token: TokenData = Depends(verify_token)):
    aprendices_with_roll = aprendices_service.get_all_aprendices()
    return JSONResponse(status_code=200, content=jsonable_encoder(aprendices_with_roll))   

@limiter.limit("20/minute")
@aprendices_router.post("/api/v1/aprendiz-registration", tags=['Aprendices'])
async def create_aprendiz(request: Request, aprendices: Aprendices):
    result = aprendices_service.create_aprendiz(aprendices)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@aprendices_router.get("/api/v1/aprendices/id/document/{id}", tags=['Aprendices'])
def get_aprendiz_by_id(request: Request, id: int, token: TokenData = Depends(verify_token)):
    aprendiz = aprendices_service.get_aprendiz_by_id(id)
    return JSONResponse(status_code=200, content=jsonable_encoder(aprendiz))

@limiter.limit("20/minute")
@aprendices_router.get("/api/v1/aprendices/{document}", tags=['Aprendices'])
def get_aprendiz_by_document(request: Request, document: int, token: TokenData = Depends(verify_token)):
    aprendiz = aprendices_service.get_aprendiz_by_document(document)
    return JSONResponse(status_code=200, content=jsonable_encoder(aprendiz))

@limiter.limit("20/minute")
@aprendices_router.get("/api/v1/aprendiz-status/{document}", tags=['Aprendices'])
def get_aprendiz_status_by_document(request: Request, document: int):
    estado = aprendices_service.get_aprendiz_status_by_document(document)
    return JSONResponse(status_code=200, content=jsonable_encoder(estado))


@limiter.limit("20/minute")
@aprendices_router.get("/api/v1/aprendiz-status", tags=['Estatus de Aprendices'])
def get_aprendiz_status(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1),
    token: TokenData = Depends(verify_token)
):
    result = aprendices_service.get_aprendiz_status(page, per_page)
    return JSONResponse(
        status_code=200,
        content={
            "total_items": result["total_items"],
            "page": result["page"],
            "per_page": result["per_page"],
            "items": jsonable_encoder(result["items"])
        }
    )

@limiter.limit("20/minute")
@aprendices_router.get("/api/v2/aprendiz-status", tags=['Estatus de Aprendices'])
def get_aprendiz_status_v2(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1),
    token: TokenData = Depends(verify_token)
):
    """
    Endpoint v2 que devuelve solo aprendices con status_id 4, 5 o 6 de forma paginada.
    Este endpoint garantiza devolver exactamente el número de aprendices solicitado en 'per_page'
    y mejora la lógica de paginación para un funcionamiento correcto.
    """
    result = aprendices_service.get_aprendiz_status_v2(page, per_page)
    return JSONResponse(
        status_code=200,
        content={
            "total_items": result["total_items"],
            "page": result["page"],
            "per_page": result["per_page"],
            "items": jsonable_encoder(result["items"])
        }
    )

@limiter.limit("20/minute")
@aprendices_router.get("/api/v1/aprendiz-statu/{document}", tags=['Aprendices'])
def get_aprendiz_status(request: Request, document: int, token: TokenData = Depends(verify_token)):
    response_data = aprendices_service.get_aprendiz_with_vehicles(document)
    return JSONResponse(status_code=200, content=response_data)

@limiter.limit("20/minute")
@aprendices_router.put("/api/v1/aprendiz-change-status", tags=['Aprendices'])
def change_aprendiz_status(request: Request, req: ChangeStatusRequest, token: TokenData = Depends(verify_token)):
    result = aprendices_service.change_aprendiz_status(req)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@aprendices_router.put("/api/v1/aprendiz-update/{aprendiz_id}", tags=['Aprendices'])
async def update_aprendiz(request: Request, aprendiz_id: int, aprendices: Aprendices, token: TokenData = Depends(verify_token)):
    result = aprendices_service.update_aprendiz(aprendiz_id, aprendices)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
