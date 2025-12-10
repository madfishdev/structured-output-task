import json
import hashlib
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from app.services.s3_service import S3Service
from app.services.llm_service import LLMService
from app.services.cache_service import CacheService
from app.core.database import get_db
from app.services.auth_service import oauth2_scheme
from app.core.logging import logger
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

s3_service = S3Service()
llm_service = LLMService()
cache_service = CacheService()

async def get_current_username(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    from jose import JWTError, jwt
    from app.core.config import settings

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        logger.warning("Invalid JWT token received")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.post("/analyze")
async def analyze(
    prompt: str = Form(...),
    fields: str = Form(...),
    image: UploadFile = File(None),
    username: str = Depends(get_current_username)
):
    logger.info(f"Analysis request received from user: {username}")
    
    try:
        fields_list = json.loads(fields)
        logger.debug(f"Parsed {len(fields_list)} fields from request")
    except json.JSONDecodeError:
        logger.error("Invalid fields format received")
        raise HTTPException(status_code=400, detail="Invalid fields format. Must be a JSON array.")
    
    image_bytes = None
    image_type = None
    image_hash = None

    if image:
        image_bytes = await image.read()
        image_type = image.content_type
        image_hash = hashlib.sha256(image_bytes).hexdigest()
        logger.debug(f"Image received: {image.filename}, type: {image_type}, hash: {image_hash[:16]}...")

        if image_type not in ["image/jpeg", "image/png"]:
            logger.warning(f"Invalid image format rejected: {image_type}")
            raise HTTPException(status_code=400, detail="Invalid image format.")

        await s3_service.upload_image(image_bytes, image.filename, image_type, username)

    cache_result = await cache_service.get(username, prompt, fields_list, image_hash)
    if cache_result:
        logger.info(f"Returning cached result for user: {username}")
        return cache_result

    try:
        llm_result = await llm_service.analyze(prompt, fields_list, image_bytes, image_type)
    except Exception as e:
        logger.error(f"LLM analysis failed for user {username}: {str(e)}")
        raise HTTPException(status_code=500, detail="LLM analysis failed.") from e
    
    await cache_service.set(username, prompt, fields_list, image_hash, llm_result)

    logger.info(f"Analysis completed successfully for user: {username}")
    return llm_result