from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    print("TOKEN:",token)
    user = decode_token(token)
    print("USER:", user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user
