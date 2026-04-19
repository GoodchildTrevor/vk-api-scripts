from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    vk_token: str
    vk_api_version: str = "5.199"
    vk_base_url: str = "https://api.vk.com/method/"
    vk_request_delay: float = 0.4

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
