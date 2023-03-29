import jwt
from ..client.Secret import *

def check_permission_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        expiration = payload.get("exp")       
        return {"username": username, "role": role}
    except jwt.DecodeError:
        return None