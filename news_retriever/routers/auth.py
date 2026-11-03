from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import hashlib
import json
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])
os.makedirs("data", exist_ok=True)
DB_FILE = "data/user_database.json"

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

class UserRegister(BaseModel):
    username: str
    password: str

class PasswordChange(BaseModel):
    new_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    db = load_user_database()
    if token not in db:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return token

async def get_admin_user(current_user: str = Depends(get_current_user)):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Permission denied: Admin access required")
    return current_user

@router.post("/register", summary="用户注册")
async def register(user_data: UserRegister):
    db = load_user_database()
    if user_data.username == "admin":
        raise HTTPException(status_code=400, detail="Username is RESERVED!")
    if user_data.username in db:
        raise HTTPException(status_code=400, detail="Username is ALREADY TAKEN!")
    
    db[user_data.username] = hash_password(user_data.password)
    save_user_database(db)
    return {"status": "success", "message": "✅ User registered successfully!"}

@router.post("/login", summary="用户登录 (获取Token)")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = load_user_database()
    if form_data.username in db and db[form_data.username] == hash_password(form_data.password):
        return {"access_token": form_data.username, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.delete("/delete_account", summary="注销当前账号")
async def delete_account(current_user: str = Depends(get_current_user)):
    db = load_user_database()
    if current_user in db:
        del db[current_user]
        save_user_database(db)
        return {"status": "success", "message": "Account deleted."}
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/admin/users", summary="管理员-查看所有用户")
async def list_users(admin: str = Depends(get_admin_user)):
    db = load_user_database()
    return {"total": len(db), "users": list(db.keys())}

@router.post("/admin/add_user", summary="管理员-添加用户")
async def admin_add_user(user_data: UserRegister, admin: str = Depends(get_admin_user)):
    db = load_user_database()
    if user_data.username in db:
        raise HTTPException(status_code=400, detail="User already exists")
    db[user_data.username] = hash_password(user_data.password)
    save_user_database(db)
    return {"status": "success", "message": f"✅ User {user_data.username} ADDED!"}

@router.delete("/admin/remove_user/{username}", summary="管理员-删除指定用户")
async def admin_remove_user(username: str, admin: str = Depends(get_admin_user)):
    db = load_user_database()
    if username in db:
        del db[username]
        save_user_database(db)
        return {"status": "success", "message": f"✅ User {username} REMOVED!"}
    raise HTTPException(status_code=404, detail="User does not exist")

@router.post("/admin/change_password", summary="管理员-修改密码")
async def admin_change_password(pwd_data: PasswordChange, admin: str = Depends(get_admin_user)):
    db = load_user_database()
    if len(pwd_data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long!")
    db["admin"] = hash_password(pwd_data.new_password)
    save_user_database(db)
    return {"status": "success", "message": "✅ Admin password changed!"}