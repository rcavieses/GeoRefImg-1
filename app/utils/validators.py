import re

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> bool:
    """Valida formato de username"""
    pattern = r'^[a-zA-Z0-9_-]{3,20}$'
    return re.match(pattern, username) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """Valida seguridad de contraseña"""
    if len(password) < 8:
        return False, "Mínimo 8 caracteres"
    if not any(char.isupper() for char in password):
        return False, "Debe contener al menos una mayúscula"
    if not any(char.isdigit() for char in password):
        return False, "Debe contener al menos un número"
    return True, "OK"

def validate_coordinates(lat: float, lng: float) -> bool:
    """Valida coordenadas geográficas"""
    return -90 <= lat <= 90 and -180 <= lng <= 180
