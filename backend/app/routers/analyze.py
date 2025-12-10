import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.services.s3_service import S3Service
from app.services.llm_service import LLMService
from app.core.database import get_db
from app.services.auth_service import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

async def get_current_username(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    from jose import JWTError, jwt
    from app.core.config import settings

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/analyze")
async def analyze(
    prompt: str = Form(...),
    fields: str = Form(...),
    image: UploadFile = File(None),
    username: str = Depends(get_current_username)
):
    if image and image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format.")
    
    try:
        fields_list = json.loads(fields)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid fields format. Must be a JSON array.")
    
    image_bytes = await image.read() if image else None

    s3_service = S3Service()

    try:
        _ = await s3_service.upload_image(image_bytes, image.filename, image.content_type, username) if image_bytes else None
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload image.") from e
    
    llm_service = LLMService()
    llm_result = llm_service.analyze(prompt, fields_list, image_bytes, image.content_type if image else None)
    return llm_result