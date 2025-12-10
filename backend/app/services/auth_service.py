from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.core.config import settings
from app.schemas.schemas import UserLogin, UserRegister
from app.models import User

import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return password_context.hash(password)
    
    async def authenticate_user(self, user_login: UserLogin):
        result = await self.db.execute(select(User).where(User.username == user_login.username))
        user = result.scalar_one_or_none()
        if not user:
            return False
        if not self.verify_password(user_login.password, user.hashed_password):
            return False
        return user
    
    async def register_user(self, user_register: UserRegister):
        result = await self.db.execute(select(User).where(User.username == user_register.username))
        user = result.scalar_one_or_none()
        if user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = self.get_password_hash(user_register.password)
        new_user = User(username=user_register.username, hashed_password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt