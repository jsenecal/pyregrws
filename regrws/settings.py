from pydantic import HttpUrl, SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    base_url: HttpUrl
    api_key: SecretStr
    model_config = SettingsConfigDict(env_prefix="regrws_")
