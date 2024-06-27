from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from config.database import engine, Base
from fastapi.security import OAuth2PasswordRequestForm
from routers.qr_route import qr_router
from routers.aprendices_route import aprendices_router
from routers.users_route import user_router
from routers.vigilante_route import vigilante_router
from routers.admins_route import admins_router
from routers.vehicles_route import vehicle_router
from routers.tickets_route import tickets_route
from routers.upleader_s3 import upload_to_s3_route



app = FastAPI()
app.title = "Parqueo API"
app.version = "0.0.1"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  
    allow_headers=["*"],
)
app.include_router(qr_router)
app.include_router(aprendices_router)
app.include_router(user_router)
app.include_router(vigilante_router)
app.include_router(admins_router)
app.include_router(vehicle_router)
app.include_router(tickets_route)
app.include_router(upload_to_s3_route)








Base.metadata.create_all(bind=engine)
