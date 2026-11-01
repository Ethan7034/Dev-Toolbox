from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib
import json
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])

security = HTTPBearer()
DB_FILE = "user_database.json"

def save_user_database(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def load_user_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    default_db = {"admin": hash_password("123456")}
    save_user_database(default_db)
    return default_db

def hash_password(password: str):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token.startswith("token_for_"):
        raise HTTPException(status_code=401, detail="Invalid Token")
    return token.replace("token_for_", "")

@router.post("/login", summary="🔑")
async def login(
    username: str = Form(..., description="请输入用户名 (默认: admin)"),
    password: str = Form(..., description="请输入密码 (默认: 123456)")
):
    db = load_user_database()
    
    if username in db and db[username] == hash_password(password):
        return {"access_token": f"token_for_{username}", "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Incorrect username or password")