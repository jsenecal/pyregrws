from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the regrws library.

    This class handles configuration through environment variables with the
    'regrws_' prefix or through direct instantiation.

    Attributes:
        base_url: The base URL for the ARIN Reg-RWS API.
        api_key: Your ARIN API key (stored securely as SecretStr).

    Environment Variables:
        REGRWS_BASE_URL: Base URL for the API
        REGRWS_API_KEY: Your ARIN API key

    Example:
        >>> settings = Settings(
        ...     base_url="https://reg.arin.net/rws",
        ...     api_key="your-api-key"
        ... )
    """

    model_config = SettingsConfigDict(env_prefix="regrws_")

    base_url: HttpUrl
    api_key: SecretStr
