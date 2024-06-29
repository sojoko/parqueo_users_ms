from jwt import encode
from datetime import datetime, timedelta, timezone


def create_tokens(data: dict, access_token_expires_delta: int = 30, refresh_token_expires_delta: int = 3 * 24 * 60):
    
    access_token_payload = data.copy()
    access_token_payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=access_token_expires_delta)
    access_token = encode(payload=access_token_payload, key="access_secret", algorithm="HS256")

    refresh_token_payload = data.copy()
    refresh_token_payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=refresh_token_expires_delta)
    refresh_token = encode(payload=refresh_token_payload, key="refresh_secret", algorithm="HS256")

    return access_token, refresh_token
