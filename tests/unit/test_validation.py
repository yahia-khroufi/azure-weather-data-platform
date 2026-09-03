from src.quality.validation import is_valid_weather_payload


def test_valid_weather_payload():
    payload = {"name": "Fes", "main": {"temp": 25.4, "humidity": 40}}

    assert is_valid_weather_payload(payload)


def test_invalid_weather_payload():
    payload = {"name": "Fes", "main": {"temp": 25.4, "humidity": 150}}

    assert not is_valid_weather_payload(payload)
