def is_valid_weather_payload(payload: dict) -> bool:
    """Vérifie quelques champs importants de la réponse OpenWeather."""
    if not payload.get("name"):
        return False

    main = payload.get("main")
    if not isinstance(main, dict):
        return False

    temperature = main.get("temp")
    if not isinstance(temperature, (int, float)):
        return False

    humidity = main.get("humidity")
    if not isinstance(humidity, (int, float)):
        return False
    if humidity < 0 or humidity > 100:
        return False

    return True
