import pytest

from src.utils.settings import get_settings


def test_get_settings(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-key")
    monkeypatch.setenv("AZURE_SUBSCRIPTION_ID", "test-subscription")
    monkeypatch.setenv("OPENWEATHER_CURRENT_URL", "https://example.com/weather")
    monkeypatch.setenv("PATH_CITIES", "config/cities.json")
    monkeypatch.setenv("DEFAULT_TIMEOUT_SECONDS", "20")

    settings = get_settings()

    assert settings.openweather_api_key == "test-key"
    assert settings.azure_subscription_id == "test-subscription"
    assert settings.path_cities == "config/cities.json"
    assert settings.timeout == 20


def test_get_settings_rejects_invalid_timeout(monkeypatch):
    monkeypatch.setenv("DEFAULT_TIMEOUT_SECONDS", "abc")

    with pytest.raises(ValueError):
        get_settings()
