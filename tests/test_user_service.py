from app.services.user_service import UserService
from app.utils.validators import validate_username, validate_email

def test_validate_username():
    """Test validación de username"""
    assert validate_username("validuser") == True
    assert validate_username("ab") == False  # Muy corto
    assert validate_username("user@123") == False  # Carácter inválido

def test_validate_email():
    """Test validación de email"""
    assert validate_email("user@example.com") == True
    assert validate_email("invalid.email") == False
    assert validate_email("test@domain.co.uk") == True

def test_create_user(db):
    """Test creación de usuario"""
    user = UserService.create_user(
        db,
        username="testuser",
        email="test@example.com",
        password="TestPassword123",
        first_name="Test",
        last_name="User"
    )
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.first_name == "Test"

def test_authenticate_user(db):
    """Test autenticación de usuario"""
    # Crear usuario
    UserService.create_user(
        db,
        username="authuser",
        email="auth@example.com",
        password="TestPassword123"
    )
    
    # Autenticar
    user = UserService.authenticate_user(db, "authuser", "TestPassword123")
    assert user.username == "authuser"
