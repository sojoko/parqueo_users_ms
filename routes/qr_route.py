from fastapi import APIRouter, Depends, HTTPException
from jwt_manager import TokenData, verify_token
from utils.rate_limiter import limiter
from schemas.qr import QR 
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Request
from services.qr_service import QRService


qr_router = APIRouter()
qr_service = QRService()

@limiter.limit("20/day")
@limiter.limit("10/hour")
@qr_router.post("/api/v1/qr", tags=['QR'])
def create_qr(request:Request, qr: QR, document: int, token: TokenData = Depends(verify_token)):
    qr_code = qr_service.create_qr(qr, document)
    return JSONResponse(status_code=200, content=jsonable_encoder(qr_code))

@limiter.limit("20/minute")
@qr_router.get("/api/v1/generate-report", tags=['Report'], response_class=FileResponse)
async def generate_report(request:Request):
    pdf_file = qr_service.generate_report()
    return pdf_file
