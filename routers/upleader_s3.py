from fastapi import APIRouter, HTTPException, File, UploadFile
from datetime import datetime, timedelta
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from jwt_manager import TokenData, verify_token
from models.admins import Admins as AdminModel
from schemas.admins import Admins
from fastapi import Depends, HTTPException, status
import boto3
import dotenv
import os

dotenv.load_dotenv()
s3_cliente = boto3.client('s3', aws_access_key_id = str(os.getenv("AWS_ACCESS_KEY")), aws_secret_access_key = str(os.getenv("AWS_SECRET_KEY")))
upload_to_s3_route = APIRouter()


@upload_to_s3_route.post("/api/v1/upload_img_s3", tags=['upload_img_s3'])
async def upload_img_to_s3(image: UploadFile = File(...)):  
    bucket_url = 'https://d351ygrurko1q2.cloudfront.net/'
    try:
        object_name = image.filename     
        image_data = await image.read()
        public_url = f"{bucket_url}{object_name}"
        s3_cliente.put_object(Body=image_data, Bucket="parqueo-assets", Key=object_name)
        return JSONResponse(status_code=200, content=jsonable_encoder({"message": "Imagen subida correctamente", "url": public_url}))
    except Exception as e:        
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")