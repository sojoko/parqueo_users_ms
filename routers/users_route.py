from fastapi import APIRouter, HTTPException
from models.users import User as UserModel
from models.users import UserStatus, UserRoll
from schemas.usersLogin import User
from schemas.usersRegistry import UserRegistry
from fastapi.encoders import jsonable_encoder
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from models.aprendices import Aprendices as AprendizModel
from jwt_manager import create_tokens
from models.admins import Admins as AdminModel
from fastapi import FastAPI, HTTPException
from fastapi import Depends, HTTPException, status


user_router = APIRouter()


@user_router.get("/api/v1/users/{document}", tags=['Users'])
def get_user(document: int):
    db = Session()  
    user = db.query(UserModel).filter(UserModel.document == document).first()
    return JSONResponse(status_code=200, content=jsonable_encoder(user))


@user_router.post("/api/v1/login", tags=['Auth'])
def login(users: User):
    users.password = int(users.password)
    users.document = int(users.document)
    db = Session()
    user = db.query(UserModel).filter(UserModel.document == users.document).first()
    if not user or not int(user.password) == users.password:        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    roll = db.query(UserModel).filter(UserModel.document == users.document).first().roll_id
    
    if roll == 1:
        name = db.query(AdminModel).filter(AdminModel.document == users.document).first().name
    elif roll == 2:
        name = db.query(AprendizModel).filter(AprendizModel.document == users.document).first().name
    

    user_for_token = {"document": user.document, "password": user.password}
    token = create_tokens(data=user_for_token)
    access_token = token[0]
    refresh_token = token[1] 
    return JSONResponse(status_code=200, content=jsonable_encoder({"name": name, "document": users.document, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user_roll": roll}))


@user_router.post("/api/v1/create_user", tags=['Users'])

def create_user(users: UserRegistry):
    db = Session()
    users.password = int(users.password)
    users.document = int(users.document)
    status_default = 1
    user_exist = db.query(UserModel).filter(UserModel.document == users.document).first()
    if user_exist:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
            )
    try:      
        new_user = UserModel(
            document=users.document,
            password=users.password,
            state_id=status_default,
            roll_id=users.roll_id,
        )
        db.add(new_user)
        db.commit()
        return {"message": "El usuario fue registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")