from pydantic import SecretStr, RedisDsn, AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: SecretStr
    admin_id: int

    redis_url: RedisDsn
    gradio_url: str

    class Config:
        override = False
        env_file = ".env"
        env_prefix = "BOT_"
        extra = "allow"


settings = Settings()
