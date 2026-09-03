import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CITIES_PATH = PROJECT_ROOT / "config" / "cities.json"


def load_cities(path: str | Path = DEFAULT_CITIES_PATH) -> list[str]:
    """Charge la liste des villes depuis un fichier JSON."""
    try:
        with Path(path).open(encoding="utf-8") as file:
            city_items = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {path}") from None
    except json.JSONDecodeError:
        raise ValueError("Le fichier des villes contient un JSON invalide") from None

    if not isinstance(city_items, list):
        raise ValueError("Le fichier des villes doit contenir une liste")

    cities = []
    for item in city_items:
        if not isinstance(item, dict) or not item.get("city"):
            raise ValueError("Chaque élément doit contenir une ville")
        cities.append(item["city"])

    return cities
