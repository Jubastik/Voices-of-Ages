from pydantic import SecretStr, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: SecretStr
    admin_id: int

    redis_url: RedisDsn

    class Config:
        override = False
        env_file = ".env"
        env_prefix = "BOT_"


settings = Settings()
