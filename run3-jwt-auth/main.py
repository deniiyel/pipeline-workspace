import hashlib
import time
import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

app = FastAPI(title="JWT Auth & User Service")

SECRET_KEY = "super-secret-production-key-change-me"
ALGORITHM = "HS256"
DB_NAME = "auth.db"

security = HTTPBearer()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def create_access_token(data: dict, expires_delta: int = 3600) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": int(time.time()) + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if not user.username.strip() or not user.password.strip():
        raise HTTPException(status_code=400, detail="Username and password cannot be empty")
    
    hashed_pw = hash_password(user.password)
    conn = sqlite3.connect(DB_NAME, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (user.username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()
    return {"message": "User registered successfully"}

@app.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    hashed_pw = hash_password(user.password)
    conn = sqlite3.connect(DB_NAME, timeout=10)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (user.username,))
        row = cursor.fetchone()
    finally:
        conn.close()

    if not row or row[0] != hashed_pw:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"status": "authenticated", "username": current_user}