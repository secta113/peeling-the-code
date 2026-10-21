"""4章：環境で変わる値に、門を立てる（pydantic-settings）。"""

from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", frozen=True)

    db_path: Path
    mail_api_url: HttpUrl
    retry: int = 3
