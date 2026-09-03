import json

import pytest

from src.utils.config import load_cities


def test_load_cities(tmp_path):
    path = tmp_path / "cities.json"
    path.write_text(
        json.dumps([{"city": "Fes"}, {"city": "Rabat"}]),
        encoding="utf-8",
    )

    assert load_cities(path) == ["Fes", "Rabat"]


def test_load_cities_raises_error_when_json_is_not_a_list(tmp_path):
    path = tmp_path / "cities.json"
    path.write_text(json.dumps({"city": "Fes"}), encoding="utf-8")

    with pytest.raises(ValueError):
        load_cities(path)


def test_load_cities_rejects_missing_city(tmp_path):
    path = tmp_path / "cities.json"
    path.write_text(json.dumps([{"name": "Fes"}]), encoding="utf-8")

    with pytest.raises(ValueError):
        load_cities(path)
