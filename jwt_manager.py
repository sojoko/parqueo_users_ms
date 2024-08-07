from jwt import encode
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

SECRET_KEY = "access_secret" 
ALGORITHM = "HS256"


def create_tokens(data: dict, access_token_expires_delta: int = 30, refresh_token_expires_delta: int = 3 * 24 * 60):
    
    access_token_payload = data.copy()
    access_token_payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=access_token_expires_delta)
    access_token = encode(payload=access_token_payload, key="access_secret", algorithm="HS256")

    refresh_token_payload = data.copy()
    refresh_token_payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=refresh_token_expires_delta)
    refresh_token = encode(payload=refresh_token_payload, key="refresh_secret", algorithm="HS256")

    return access_token, refresh_token


class TokenData(BaseModel):
    document: Optional[int] = None

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        document: int = payload.get("document")
        if document is None:
            raise credentials_exception
        token_data = TokenData(document=document)
    except JWTError:
        raise credentials_exception
    return token_data