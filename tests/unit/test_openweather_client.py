from unittest.mock import Mock

import pytest
import requests

from src.ingestion.openweather_client import (
    DEFAULT_TIMEOUT_SECONDS,
    OPENWEATHER_CURRENT_URL,
    get_current_weather,
)


def test_get_current_weather():
    expected = {"name": "Fes", "main": {"temp": 21.5, "humidity": 52}}
    response = Mock()
    response.json.return_value = expected
    session = Mock()
    session.get.return_value = response

    actual = get_current_weather("Fes", "test-key", session)

    assert actual == expected
    session.get.assert_called_once_with(
        OPENWEATHER_CURRENT_URL,
        params={"q": "Fes", "appid": "test-key", "units": "metric"},
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )


def test_get_current_weather_raises_error():
    session = Mock()
    session.get.side_effect = requests.RequestException()

    with pytest.raises(RuntimeError):
        get_current_weather("Fes", "test-key", session)
