from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Token
from app.schemas.schemas import UserLogin, UserRegister
from app.core.database import get_db
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)

    user = await auth_service.authenticate_user(form_data)
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth_service.create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=Token)
async def register(user_register: UserRegister, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)

    try :
        user = await auth_service.register_user(user_register)
    except HTTPException as e:
        raise e
    
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }