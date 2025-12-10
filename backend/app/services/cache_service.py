import json
import hashlib

from typing import Optional
from redis.asyncio import Redis
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.REDIS_URL)
        self.default_ttl = settings.REDIS_CACHE_TTL_SECONDS

    def _generate_key(self, username: str, prompt: str, fields: list, image_hash: Optional[str]) -> str:
        fields_sorted = sorted(fields, key=lambda x: x['name'])
        key_data = {
            "username": username,
            "prompt": prompt,
            "fields": ", ".join([f"'{f['name']}' (type: {f['type']})" for f in fields_sorted]),
            "image_hash": image_hash
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode('utf-8')).hexdigest()
    
    async def get(self, username: str, prompt: str, fields: list, image_hash: Optional[str]) -> Optional[dict]:
        key = self._generate_key(username, prompt, fields, image_hash)
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None
    
    async def set(self, username: str, prompt: str, fields: list, image_hash: Optional[str], result: dict):
        key = self._generate_key(username, prompt, fields, image_hash)
        await self.redis_client.set(key, json.dumps(result), ex=self.default_ttl)