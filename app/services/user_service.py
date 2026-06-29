from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.validators import validate_email, validate_username
from app.utils.exceptions import ValidationException, AuthException, NotFoundException

class UserService:
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str, first_name: str = None, last_name: str = None) -> User:
        """Crea un nuevo usuario"""
        # Validar
        if not validate_username(username):
            raise ValidationException("Username inválido (3-20 caracteres, solo alfanuméricos y guiones)")
        if not validate_email(email):
            raise ValidationException("Email inválido")
        
        # Verificar si existe
        existing = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing:
            raise ValidationException("Username o email ya existe")
        
        # Crear usuario
        hashed_password = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Autentica un usuario"""
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            raise AuthException("Credenciales inválidas")
        return user
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """Obtiene un usuario por ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("Usuario")
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Obtiene un usuario por username"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise NotFoundException("Usuario")
        return user
