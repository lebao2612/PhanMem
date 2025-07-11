import redis.asyncio as redis
import json
import uuid

class RedisClient:
    def __init__(self, url: str):
        try:
            self.redis = redis.from_url(url, decode_responses=False)
        except Exception as e:
            raise RuntimeError("Redis configuration error.") from e

    async def set_bytes(self, key: str, data: bytes, expire: int = None):
        try:
            await self.redis.set(name=key, value=data, ex=expire)
        except Exception as e:
            raise RuntimeError(f"Failed to set Redis key: {key}") from e

    async def get_bytes(self, key: str) -> bytes | None:
        try:
            return await self.redis.get(name=key)
        except Exception as e:
            raise RuntimeError(f"Failed to get Redis key: {key}") from e

    async def delete(self, key: str):
        try:
            await self.redis.delete(key)
        except Exception as e:
            raise RuntimeError(f"Failed to delete Redis key: {key}") from e

    async def set_json(self, key: str, data: dict, expire: int|None = None):
        try:
            json_data = json.dumps(data).encode()
            await self.set_bytes(key, json_data, expire)
        except Exception as e:
            raise RuntimeError(f"Failed to set JSON Redis key: {key}") from e

    async def get_json(self, key: str) -> dict | None:
        try:
            raw = await self.get_bytes(key)
            if raw is None:
                return None
            return json.loads(raw.decode())
        except Exception as e:
            raise RuntimeError(f"Failed to get JSON Redis key: {key}") from e

    def generate_key(self, prefix: str = "temp", suffix: str|None = None) -> str:
        uid = uuid.uuid4().hex
        return f"{prefix}:{suffix or uid}"
