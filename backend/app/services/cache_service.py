import json
import hashlib

from typing import Optional
from redis.asyncio import Redis
from app.core.config import settings
from app.core.logging import logger

class CacheService:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.REDIS_URL)
        self.default_ttl = settings.REDIS_CACHE_TTL_SECONDS
        logger.info(f"Cache service initialized with TTL: {self.default_ttl}s")

    def _generate_key(self, username: str, prompt: str, fields: list, image_hash: Optional[str]) -> str:
        fields_sorted = sorted(fields, key=lambda x: x['name'])
        key_data = {
            "username": username,
            "prompt": prompt,
            "fields": ", ".join([f"'{f['name']}' (type: {f['type']})" for f in fields_sorted]),
            "image_hash": image_hash
        }
        key_string = json.dumps(key_data, sort_keys=True)
        cache_key = hashlib.sha256(key_string.encode('utf-8')).hexdigest()
        logger.debug(f"Generated cache key: {cache_key[:16]}... for user: {username}")
        return cache_key
    
    async def get(self, username: str, prompt: str, fields: list, image_hash: Optional[str]) -> Optional[dict]:
        key = self._generate_key(username, prompt, fields, image_hash)
        cached_data = await self.redis_client.get(key)
        if cached_data:
            logger.info(f"Cache HIT for user: {username}")
            return json.loads(cached_data)
        logger.info(f"Cache MISS for user: {username}")
        return None
    
    async def set(self, username: str, prompt: str, fields: list, image_hash: Optional[str], result: dict):
        key = self._generate_key(username, prompt, fields, image_hash)
        await self.redis_client.set(key, json.dumps(result), ex=self.default_ttl)
        logger.info(f"Cache SET for user: {username} (TTL: {self.default_ttl}s)")