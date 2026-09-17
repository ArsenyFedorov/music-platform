from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str

@lru_cache
def get_settings() -> Settings:
    """Возвращает кэшированный объект настроек"""

    return Settings()