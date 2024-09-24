from os import getenv

from dotenv import load_dotenv

from app.core.config import Settings, AuthSettings, RedisSettings

load_dotenv(getenv("ENV_FILE"))
settings = Settings()

auth_settings = AuthSettings()
redis_settings = RedisSettings()
# s()
# auth_settings.algorithm =