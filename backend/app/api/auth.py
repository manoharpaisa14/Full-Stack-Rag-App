from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from app.utils.jwt import create_access_token
from app.utils.auth import get_current_user
import redis
import json

router = APIRouter()
r = redis.Redis(host="redis", port=6379, decode_responses=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserSignup(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup(user: UserSignup):
    if r.exists(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = pwd_context.hash(user.password)
    user_data = {
        "username": user.username,
        "password": hashed_password
    }
    r.set(user.username, json.dumps(user_data))
    return {"message": "User created"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user_data = r.get(form.username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    user = json.loads(user_data)
    if not pwd_context.verify(form.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/verify-token")
def verify_token(user: dict = Depends(get_current_user)):
    if isinstance(user, dict) and "sub" in user:
        return {"valid": True, "username": user["sub"]}
    else:
        return {"valid": False}
