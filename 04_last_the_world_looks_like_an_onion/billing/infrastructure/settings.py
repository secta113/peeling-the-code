"""環境で変わる値の門（pydantic-settings）。"""

from pathlib import Path

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", frozen=True)

    db_path: Path
    mail_api_url: HttpUrl
    retry: int = 3
