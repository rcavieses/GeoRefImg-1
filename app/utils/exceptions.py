import json
from typing import Any, Dict

class CustomException(Exception):
    """Excepción base personalizada"""
    def __init__(self, message: str, code: str = "ERROR", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)

class DatabaseException(CustomException):
    """Error en operación de BD"""
    def __init__(self, message: str):
        super().__init__(message, "DB_ERROR", 500)

class ValidationException(CustomException):
    """Error de validación"""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", 400)

class AuthException(CustomException):
    """Error de autenticación"""
    def __init__(self, message: str):
        super().__init__(message, "AUTH_ERROR", 401)

class GeometryException(CustomException):
    """Error geométrico"""
    def __init__(self, message: str):
        super().__init__(message, "GEOMETRY_ERROR", 400)

class NotFoundException(CustomException):
    """Recurso no encontrado"""
    def __init__(self, resource: str):
        super().__init__(f"{resource} no encontrado", "NOT_FOUND", 404)
