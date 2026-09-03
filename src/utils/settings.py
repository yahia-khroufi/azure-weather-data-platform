import os
from dataclasses import dataclass

from dotenv import load_dotenv

DEFAULT_OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITIES_PATH = "config/cities.json"
DEFAULT_TIMEOUT_SECONDS = 15


@dataclass
class Settings:
    openweather_api_key: str
    azure_subscription_id: str
    base_url: str
    path_cities: str
    timeout: int


def get_settings() -> Settings:
    load_dotenv()

    timeout_value = os.getenv("DEFAULT_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS))
    try:
        timeout = int(timeout_value)
    except ValueError:
        raise ValueError("DEFAULT_TIMEOUT_SECONDS doit être un nombre") from None

    return Settings(
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY", ""),
        azure_subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID", ""),
        base_url=os.getenv("OPENWEATHER_CURRENT_URL") or DEFAULT_OPENWEATHER_URL,
        path_cities=os.getenv("PATH_CITIES") or DEFAULT_CITIES_PATH,
        timeout=timeout,
    )


settings = get_settings()
