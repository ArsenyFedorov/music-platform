from pydantic_settings import SettingsConfigDict, BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    database_url: str
    jwt_secret: str
    access_token_expire_minutes: int = 30

@lru_cache
def get_settings() -> Settings:
    """Возвращает кэшированный объект настроек"""

    return Settings()