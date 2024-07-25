from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from config.database import engine, Base
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routers.qr_route import qr_router
from routers.aprendices_route import aprendices_router
from routers.users_route import user_router
from routers.vigilante_route import vigilante_router
from routers.admins_route import admins_router
from routers.vehicles_route import vehicle_router
from routers.tickets_route import tickets_route
from routers.upleader_s3 import upload_to_s3_route
from routers.parking import parking_router
from fastapi.openapi.utils import get_openapi

app = FastAPI()
app.title = "Parqueo API"
app.version = "0.0.1"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://parqueo-frt.pages.dev", "https://parqueo-frt.pages.dev/"], 
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
app.include_router(parking_router)

@app.get("/")
def read_root():
    return {"message": "PARQUEO API"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Parqueo API",
        version="0.0.1",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")



Base.metadata.create_all(bind=engine)
