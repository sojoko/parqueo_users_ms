from fastapi import APIRouter, HTTPException, Query, Request

from main import limiter
from models.users import User as UserModel
from schemas.usersLogin import User
from schemas.usersRegistry import UserRegistry
from fastapi.encoders import jsonable_encoder
from config.database import engine, Base, Session
from fastapi.responses import HTMLResponse, JSONResponse
from models.aprendices import Aprendices as AprendizModel
from models.vigilantes import Vigilantes as VigilanteModel
from jwt_manager import TokenData, create_tokens, verify_token
from models.admins import Admins as AdminModel
from fastapi import Depends, HTTPException, status
import bcrypt

user_router = APIRouter()

@limiter.limit("20/minute")
@user_router.get("/api/v1/users/{document}", tags=['Users'])
def get_user(request:Request, document: int, token: TokenData = Depends(verify_token)):
    db = Session()
    try:
        user = db.query(UserModel).filter(UserModel.document == document).first()        
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")        
        return JSONResponse(status_code=200, content=jsonable_encoder(user))    
    except HTTPException as http_exc:   
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close()

@limiter.limit("20/minute")
@user_router.delete("/api/v1/users/delete/{document}/{roll}", tags=['Users']) 
def delete_user(request:Request, document: int, roll: int, token: TokenData = Depends(verify_token)):
    db = Session()
   
    try:
        user = None
        if roll == 1:
            user = db.query(AdminModel).filter(AdminModel.document == document).first()
        elif roll == 2:
            user = db.query(AprendizModel).filter(AprendizModel.document == document).first()
        elif roll == 3:
            user = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()
        else:
            raise HTTPException(status_code=400, detail="Rol no válido")
        
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        db.delete(user)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Usuario eliminado con éxito"})
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()
        
@limiter.limit("20/minute")
@user_router.get("/api/v1/users_all", tags=['Users'])
def get_user_all(request:Request):
    db = Session()
    try:
        users = db.query(UserModel).all()        
        if not users:
            raise HTTPException(status_code=404, detail="No se encontraron usuarios")        
        return JSONResponse(status_code=200, content=jsonable_encoder(users))
    
    except HTTPException as http_exc:    
        raise http_exc
    except Exception as e:     
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close() 

@limiter.limit("20/minute")
@user_router.post("/api/v1/login", tags=['Auth'])
def login(request:Request, users: User):
    db = Session()
    try:    
        users.password = str(users.password)
        users.document = int(users.document)       
  
        user = db.query(UserModel).filter(UserModel.document == users.document).first()
        
        if not user or not bcrypt.checkpw(users.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
            )             
        roll = user.roll_id        
      
        if roll == 1:
            name = db.query(AdminModel).filter(AdminModel.document == users.document).first().name
        elif roll == 2:
            name = db.query(AprendizModel).filter(AprendizModel.document == users.document).first().name
        elif roll == 3:
            name = db.query(VigilanteModel).filter(VigilanteModel.document == users.document).first().name
    
        user_for_token = {"document": user.document, "password": user.password}
        access_token, refresh_token = create_tokens(data=user_for_token)
        
        return JSONResponse(status_code=200, content=jsonable_encoder({
            "name": name,
            "document": users.document,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_roll": roll
        }))    
    except HTTPException as http_exc:      
        raise http_exc
    except Exception as e:       
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")    
    finally:
        db.close()  


@limiter.limit("20/minute")
@user_router.post("/api/v1/create_user", tags=['Users'])
def create_user(request:Request, users: UserRegistry):
    db = Session()
    users.password = str(users.password)
    users.document = str(users.document)
    status_default = 1
    user_exist = db.query(UserModel).filter(UserModel.document == users.document).first()
    if user_exist:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
            )
    try:        
        hashed_password = bcrypt.hashpw(users.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')    
        new_user = UserModel(
            document=users.document,
            password=hashed_password,
            state_id=status_default,
            roll_id=users.roll_id,
        )
        db.add(new_user)
        db.commit()
        return {"message": "El usuario fue registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()  

@limiter.limit("20/minute")
@user_router.get("/api/v1/all-persons", tags=['Users'])
async def get_all_persons(
    request:Request,
    page: int = Query(1, ge=1), 
    per_page: int = Query(5, ge=1,),
    token: TokenData = Depends(verify_token)
):
    try:
        db = Session()
        try:         
            skip = (page - 1) * per_page

            total_vigilantes = db.query(VigilanteModel).count()
            total_aprendices = db.query(AprendizModel).count()
            total_admins = db.query(AdminModel).count()

            vigilants = db.query(VigilanteModel).offset(skip).limit(per_page).all()
            aprendices = db.query(AprendizModel).offset(skip).limit(per_page).all()
            admins = db.query(AdminModel).offset(skip).limit(per_page).all()

        
            vigilantes_with_roll = [{'roll': 'vigilante', **vigilante.__dict__} for vigilante in vigilants]
            aprendices_with_roll = [{'roll': 'aprendiz', **aprendiz.__dict__} for aprendiz in aprendices]
            admins_with_roll = [{'roll': 'admin', **admin.__dict__} for admin in admins]

      
            unidos = vigilantes_with_roll + aprendices_with_roll + admins_with_roll
            total_items = total_vigilantes + total_aprendices + total_admins

            return JSONResponse(
                status_code=200, 
                content={
                    "total_items": total_items,
                    "page": page,
                    "per_page": per_page,
                    "items": jsonable_encoder(unidos)
                }
            )
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    
    
@limiter.limit("20/minute")
@user_router.get("/api/v1/edit_user_by_person", tags=['Users'])
async def edit_user_by_person(request:Request, document: int, roll : int, token: TokenData = Depends(verify_token)):
    try:
        db = Session()
        try:
            if roll == 1:
                user = db.query(AdminModel).filter(AdminModel.document == document).first()
            elif roll == 2:
                user = db.query(AprendizModel).filter(AprendizModel.document == document).first()
            elif roll == 3:
                user = db.query(VigilanteModel).filter(VigilanteModel.document == document).first()
            

            return JSONResponse(status_code=200, content=jsonable_encoder("Usuario actualizado exitosamente"))
        finally:
            db.close()  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la operación: {str(e)}")
    finally:
        db.close()  

