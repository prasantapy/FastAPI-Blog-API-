from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.deps import get_db
from app import models

# 🔐 JWT config
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# 🔑 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔒 Token extractor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 👤 Get current user from token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# 🔐 Hash password
def hash_password(password: str):
    password = str(password)
    print("HASH INPUT LENGTH:", len(password))
    return pwd_context.hash(password[:72])


# 🔍 Verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# 🎟️ Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)