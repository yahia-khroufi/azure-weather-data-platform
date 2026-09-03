import json
from pathlib import Path
from charset_normalizer import from_path

result = from_path("config/cities.json").best()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CITIES_PATH = PROJECT_ROOT / "config" / "cities.json"


def load_cities(path: str | Path = DEFAULT_CITIES_PATH) -> list[str]:
    """Charge la liste des villes depuis un fichier JSON."""
    try:
        with Path(path).open(encoding=result.encoding) as file:
            cities = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {path}") from None
    except json.JSONDecodeError:
        raise ValueError("Le fichier des villes contient un JSON invalide") from None

    if not isinstance(cities, list):
        raise ValueError("Le fichier des villes doit contenir une liste")

    return cities
