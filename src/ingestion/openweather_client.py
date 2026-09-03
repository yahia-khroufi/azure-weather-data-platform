import json
from typing import Any

import requests

from src.utils.config import load_cities
from src.utils.logger import get_logger
from src.utils.settings import settings

OPENWEATHER_CURRENT_URL = settings.base_url
DEFAULT_TIMEOUT_SECONDS = settings.timeout
LOGGER = get_logger(__name__)


def get_current_weather(
    city: str,
    api_key: str,
    session: requests.Session,
) -> dict[str, Any]:
    if not city:
        raise ValueError("La ville est obligatoire")

    if not api_key:
        raise ValueError("La clé API est obligatoire")

    try:
        response = session.get(
            OPENWEATHER_CURRENT_URL,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric",
            },
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        raise RuntimeError(
            f"Erreur pendant l'appel OpenWeather pour {city}"
        ) from None


def main() -> int:
    api_key = settings.openweather_api_key
    cities = load_cities(settings.path_cities)

    LOGGER.info(
        "Fetching current weather for %d city/cities",
        len(cities),
    )

    payloads = {}

    with requests.Session() as session:
        for city in cities:
            payloads[city] = get_current_weather(
                city,
                api_key,
                session,
            )

    print(
        json.dumps(
            payloads,
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
