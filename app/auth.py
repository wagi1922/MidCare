# app/routers/auth.py
import os
from dotenv import load_dotenv # type: ignore
from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from sqlalchemy.orm import Session # type: ignore
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt # type: ignore
from passlib.context import CryptContext # type: ignore
from fastapi.security import OAuth2PasswordBearer # type: ignore
from fastapi.security.api_key import APIKeyHeader # type: ignore
from fastapi import Depends, HTTPException, status # type: ignore
from datetime import datetime, timedelta

from . import schemas, models
from .database import get_db

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login") 
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def verify_api_key(api_key: str = Depends(api_key_header)):
    import secrets 
    if not secrets.compare_digest(api_key, API_KEY): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key tidak valid",
        )
    return True 

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Gunakan 30 menit dari ACCESS_TOKEN_EXPIRE_MINUTES
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # --- TAMBAHKAN DEBUGGING INI ---
    print(f"DEBUG: Current UTC Time: {datetime.utcnow()}")
    print(f"DEBUG: Token Expires at: {expire}")
    # -------------------------------
    
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token tidak valid", headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        user_id: str = payload.get("sub") # type: ignore
        user_role: str = payload.get("role") # type: ignore
        if user_id is None: raise credentials_exception
        return {"user_id": int(user_id), "role": user_role}
    except JWTError:
        raise credentials_exception

def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Akses ditolak: Hanya Admin")
    return current_user

def get_current_normal_user(current_user: dict = Depends(get_current_user)) -> dict:
    # Membolehkan Admin mengakses fitur user jika perlu
    if current_user["role"] not in ["user", "admin"]: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Akses ditolak: Hanya User")
    return current_user

@auth_router.post("/login", response_model=schemas.TokenResponse)
async def login_for_access_token(
    request: schemas.TokenRequest, 
    db: Session = Depends(get_db),
    api_key_check: bool = Depends(verify_api_key)
    ):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password): # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username atau password salah")
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@auth_router.post("/register", response_model=schemas.TokenResponse)
async def register_user(
    new_user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    api_key_check: bool = Depends(verify_api_key)
    ): 
    if db.query(models.User).filter(models.User.username == new_user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username sudah terdaftar.")

    hashed_password = get_password_hash(new_user.password)
    db_user = models.User(username=new_user.username, hashed_password=hashed_password, role="user")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer", "role": db_user.role}

@auth_router.post("/adminreg", response_model=schemas.TokenResponse)
async def register_admin(
    new_user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    api_key_check: bool = Depends(verify_api_key)
    ): 
    if db.query(models.User).filter(models.User.username == new_user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username sudah terdaftar.")

    hashed_password = get_password_hash(new_user.password)
    db_user = models.User(username=new_user.username, hashed_password=hashed_password, role="admin")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer", "role": db_user.role}