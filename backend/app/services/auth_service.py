import jwt

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta

from app.core.config import settings
from app.schemas.schemas import UserLogin, UserRegister
from app.models import User
from app.core.logging import logger

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)
    
    def _get_password_hash(self, password: str) -> str:
        return password_context.hash(password)
    
    async def authenticate_user(self, user_login: UserLogin):
        logger.debug(f"Authentication attempt for user: {user_login.username}")
        result = await self.db.execute(select(User).where(User.username == user_login.username))
        user = result.scalar_one_or_none()
        if not user:
            logger.warning(f"Authentication failed: User not found - {user_login.username}")
            return False
        if not self._verify_password(user_login.password, user.hashed_password):
            logger.warning(f"Authentication failed: Invalid password for user - {user_login.username}")
            return False
        logger.info(f"User authenticated successfully: {user_login.username}")
        return user
    
    async def register_user(self, user_register: UserRegister):
        logger.debug(f"Registration attempt for user: {user_register.username}")
        result = await self.db.execute(select(User).where(User.username == user_register.username))
        user = result.scalar_one_or_none()
        if user:
            logger.warning(f"Registration failed: Username already exists - {user_register.username}")
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = self._get_password_hash(user_register.password)
        new_user = User(username=user_register.username, hashed_password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        logger.info(f"User registered successfully: {user_register.username}")
        return new_user
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        logger.debug(f"Access token created for: {data.get('sub')}, expires: {expire}")
        return encoded_jwt