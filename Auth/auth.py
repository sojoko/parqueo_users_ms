from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

SECRET_KEY = "access_secret"  # Debe coincidir con la clave usada para crear los tokens
ALGORITHM = "HS256"

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
