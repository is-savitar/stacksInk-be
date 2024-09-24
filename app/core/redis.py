from redis import asyncio as aioredis

from app import redis_settings

token_blocklist = aioredis.StrictRedis(
    host=redis_settings.redis_host,
    port=redis_settings.redis_port,
    db=0
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="")

async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(name=jti)
    return jti is not None