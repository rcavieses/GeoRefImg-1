import pytest
from app.services.user_service import UserService
from app.utils.security import verify_password, create_access_token, decode_token
from app.utils.exceptions import AuthException, ValidationException

class TestUserAuthentication:
    """Tests para autenticación de usuarios"""

    def test_register_new_user(self, db):
        """Test registro de nuevo usuario"""
        user = UserService.create_user(
            db,
            username="testuser",
            email="test@example.com",
            password="SecurePassword123",
            first_name="Test",
            last_name="User"
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.is_active is True
        assert user.role == "user"

    def test_register_duplicate_username(self, db):
        """Test no se puede registrar con username duplicado"""
        # Crear primer usuario
        UserService.create_user(
            db,
            username="duplicate",
            email="first@example.com",
            password="Password123"
        )

        # Intentar crear con mismo username
        with pytest.raises(ValidationException):
            UserService.create_user(
                db,
                username="duplicate",
                email="second@example.com",
                password="Password123"
            )

    def test_register_duplicate_email(self, db):
        """Test no se puede registrar con email duplicado"""
        # Crear primer usuario
        UserService.create_user(
            db,
            username="user1",
            email="duplicate@example.com",
            password="Password123"
        )

        # Intentar crear con mismo email
        with pytest.raises(ValidationException):
            UserService.create_user(
                db,
                username="user2",
                email="duplicate@example.com",
                password="Password123"
            )

    def test_authenticate_success(self, db):
        """Test autenticación exitosa"""
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
        assert user.email == "auth@example.com"

    def test_authenticate_wrong_password(self, db):
        """Test autenticación con contraseña incorrecta"""
        # Crear usuario
        UserService.create_user(
            db,
            username="authuser",
            email="auth@example.com",
            password="CorrectPassword123"
        )

        # Intentar autenticar con contraseña incorrecta
        with pytest.raises(AuthException):
            UserService.authenticate_user(db, "authuser", "WrongPassword123")

    def test_authenticate_nonexistent_user(self, db):
        """Test autenticación de usuario no existente"""
        with pytest.raises(AuthException):
            UserService.authenticate_user(db, "nonexistent", "Password123")

    def test_password_hashing(self, db):
        """Test que las contraseñas se hashean correctamente"""
        user = UserService.create_user(
            db,
            username="hashtest",
            email="hash@example.com",
            password="MyPassword123"
        )

        # Verificar que la contraseña no se almacena en texto plano
        assert user.password_hash != "MyPassword123"
        assert verify_password("MyPassword123", user.password_hash)
        assert not verify_password("WrongPassword", user.password_hash)

    def test_jwt_token_creation(self):
        """Test creación de JWT token"""
        data = {"sub": "testuser", "id": 1, "role": "user"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)

    def test_jwt_token_decode(self):
        """Test decodificación de JWT token"""
        original_data = {"sub": "testuser", "id": 1, "role": "user"}
        token = create_access_token(original_data)

        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "testuser"
        assert decoded["id"] == 1
        assert decoded["role"] == "user"

    def test_jwt_token_invalid(self):
        """Test decodificación de token inválido"""
        decoded = decode_token("invalid.token.here")
        assert decoded is None

    def test_get_user_by_id(self, db):
        """Test obtener usuario por ID"""
        user = UserService.create_user(
            db,
            username="findme",
            email="find@example.com",
            password="Password123"
        )

        retrieved = UserService.get_user(db, user.id)
        assert retrieved.id == user.id
        assert retrieved.username == "findme"

    def test_get_user_not_found(self, db):
        """Test obtener usuario inexistente"""
        from app.utils.exceptions import NotFoundException

        with pytest.raises(NotFoundException):
            UserService.get_user(db, 99999)

    def test_user_inactive(self, db):
        """Test usuario inactivo"""
        user = UserService.create_user(
            db,
            username="inactive",
            email="inactive@example.com",
            password="Password123"
        )

        # Desactivar usuario
        user.is_active = False
        db.commit()

        # Debería poder autenticarse aunque esté inactivo
        # (podemos cambiar esto si queremos validar is_active)
        authenticated = UserService.authenticate_user(db, "inactive", "Password123")
        assert authenticated.is_active is False
