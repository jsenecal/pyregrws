from pydantic import BaseSettings, HttpUrl, SecretStr


class Settings(BaseSettings):
    base_url: HttpUrl
    api_key: SecretStr

    class Config:
        env_prefix = "regrws_"
