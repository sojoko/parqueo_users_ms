from fastapi import APIRouter, HTTPException, Query, Request
from utils.rate_limiter import limiter
from schemas.usersLogin import User
from schemas.usersRegistry import UserRegistry
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import TokenData, verify_token
from fastapi import Depends, HTTPException, status
from services.users_service import UsersService

user_router = APIRouter()
users_service = UsersService()


#fachada/estructural mediator/comportamiento /singleton-estructura
@limiter.limit("20/minute")
@user_router.get("/api/v1/users/{document}", tags=['Users'])
def get_user(request:Request, document: int, token: TokenData = Depends(verify_token)):
    user = users_service.get_user(document)
    return JSONResponse(status_code=200, content=jsonable_encoder(user))

@limiter.limit("20/minute")
@user_router.delete("/api/v1/users/delete/{document}/{roll}", tags=['Users']) 
def delete_user(request:Request, document: int, roll: int, token: TokenData = Depends(verify_token)):
    result = users_service.delete_user(document, roll)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@user_router.get("/api/v1/users_all", tags=['Users'])
def get_user_all(request:Request):
    users = users_service.get_user_all()
    return JSONResponse(status_code=200, content=jsonable_encoder(users))

@limiter.limit("20/minute")
@user_router.post("/api/v1/login", tags=['Auth'])
def login(request:Request, users: User):
    result = users_service.login(users)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@limiter.limit("20/minute")
@user_router.post("/api/v1/create_user", tags=['Users'])
def create_user(request:Request, users: UserRegistry):
    result = users_service.create_user(users)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@limiter.limit("20/minute")
@user_router.get("/api/v1/all-persons", tags=['Users'])
async def get_all_persons(
    request:Request,
    page: int = Query(1, ge=1), 
    per_page: int = Query(5, ge=1,),
    token: TokenData = Depends(verify_token)
):
    result = users_service.get_all_persons(page, per_page)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@limiter.limit("20/minute")
@user_router.get("/api/v1/edit_user_by_person", tags=['Users'])
async def edit_user_by_person(request:Request, document: int, roll : int, token: TokenData = Depends(verify_token)):
    result = users_service.edit_user_by_person(document, roll)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
