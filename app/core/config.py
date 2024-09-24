from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    db_async_connection_str: str


class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_seconds: int
    refresh_token_expire_days: int


class RedisSettings(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6379
    jti_expiry: int