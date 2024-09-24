from os import getenv

from dotenv import load_dotenv

from app.core.config import Settings, AuthSettings

load_dotenv(getenv("ENV_FILE"))
settings = Settings()

# auth_settings = AuthSettingqq
# s()
# auth_settings.algorithm =