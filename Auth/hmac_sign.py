import dotenv
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.routing import APIRoute
from datetime import datetime, timedelta
import hashlib
import hmac
import os
from typing import Callable, List, Type

dotenv.load_dotenv()

API_KEY = os.getenv("USER_API_KEY")
SECRET_KEY = os.getenv("USER_SECRET_KEY")

# Lista de rutas que están exentas de la autenticación HMAC
EXEMPT_ROUTES = ["/api/v1/create_user"]

async def authenticate_api_key(
    request: Request,
    x_api_key: str = Header(None),
    x_timestamp: int = Header(None),
    x_signature: str = Header(None),
):
    """Autentica la petición para el cliente único basado en la API Key y la firma."""

    # Verificar si la ruta actual está exenta de autenticación HMAC
    if request.url.path in EXEMPT_ROUTES:
        return None

    # Si la ruta no está exenta, verificar que se proporcionaron los headers necesarios
    if x_api_key is None or x_timestamp is None or x_signature is None:
        raise HTTPException(
            status_code=401, 
            detail="Missing authentication headers. Required: x-api-key, x-timestamp, x-signature"
        )

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    timestamp = datetime.fromtimestamp(x_timestamp)
    now = datetime.now()
    if abs((now - timestamp).total_seconds()) > 300:  # 5 minutos en segundos
        raise HTTPException(status_code=401, detail="Timestamp is invalid (too old)")

    data_to_sign = f"{x_api_key}:{x_timestamp}"

    expected_signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        data_to_sign.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(x_signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    return x_api_key
