import json
from typing import Any

def dict_to_json(data: dict) -> str:
    """Convierte diccionario a JSON string"""
    return json.dumps(data, default=str)

def json_to_dict(data: str) -> dict:
    """Convierte JSON string a diccionario"""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return {}

def calculate_bbox(coordinates: list) -> dict:
    """Calcula bounding box desde coordenadas"""
    lats = [coord[1] for coord in coordinates]
    lngs = [coord[0] for coord in coordinates]
    return {
        "min_lat": min(lats),
        "max_lat": max(lats),
        "min_lng": min(lngs),
        "max_lng": max(lngs),
    }
