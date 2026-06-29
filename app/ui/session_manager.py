import streamlit as st
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.services.user_service import UserService
from app.utils.security import create_access_token, decode_token
from app.utils.exceptions import AuthException, NotFoundException

class SessionManager:
    """Gestiona sesiones de usuario en Streamlit"""
    
    @staticmethod
    def initialize_session():
        """Inicializa variables de sesión"""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "user" not in st.session_state:
            st.session_state.user = None
        if "token" not in st.session_state:
            st.session_state.token = None
        if "user_id" not in st.session_state:
            st.session_state.user_id = None
    
    @staticmethod
    def login_user(username: str, password: str) -> dict:
        """
        Autentica un usuario y crea sesión
        
        Args:
            username: Username del usuario
            password: Contraseña en texto plano
            
        Returns:
            dict con user_id, username, email, role si éxito
            
        Raises:
            AuthException si falla autenticación
        """
        db = SessionLocal()
        try:
            # Autenticar
            user = UserService.authenticate_user(db, username, password)
            
            # Crear JWT token
            access_token = create_access_token(
                data={
                    "sub": user.username,
                    "id": user.id,
                    "role": user.role
                }
            )
            
            # Guardar en session state
            st.session_state.authenticated = True
            st.session_state.user = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            }
            st.session_state.token = access_token
            st.session_state.user_id = user.id
            
            # Actualizar last_login
            user.last_login = datetime.utcnow()
            db.commit()
            
            return {
                "success": True,
                "message": "Sesión iniciada",
                "user": st.session_state.user
            }
        
        except AuthException as e:
            return {
                "success": False,
                "message": str(e.message)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
        finally:
            db.close()
    
    @staticmethod
    def register_user(username: str, email: str, password: str, first_name: str = None, last_name: str = None) -> dict:
        """
        Registra un nuevo usuario
        
        Args:
            username: Username (3-20 caracteres)
            email: Email válido
            password: Contraseña (mín 8 caracteres, mayúscula, número)
            first_name: Nombre (opcional)
            last_name: Apellido (opcional)
            
        Returns:
            dict con resultado del registro
        """
        db = SessionLocal()
        try:
            # Validar contraseña
            from app.utils.validators import validate_password
            is_valid, message = validate_password(password)
            if not is_valid:
                return {
                    "success": False,
                    "message": f"Contraseña débil: {message}"
                }
            
            # Crear usuario
            user = UserService.create_user(
                db=db,
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            return {
                "success": True,
                "message": "Usuario registrado exitosamente. Por favor, inicia sesión.",
                "user_id": user.id
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
        finally:
            db.close()
    
    @staticmethod
    def logout_user():
        """Cierra sesión del usuario actual"""
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.token = None
        st.session_state.user_id = None
    
    @staticmethod
    def is_authenticated() -> bool:
        """Verifica si el usuario está autenticado"""
        return st.session_state.get("authenticated", False)
    
    @staticmethod
    def get_current_user() -> dict | None:
        """Obtiene datos del usuario actual"""
        if st.session_state.get("authenticated"):
            return st.session_state.get("user")
        return None
    
    @staticmethod
    def get_user_id() -> int | None:
        """Obtiene ID del usuario actual"""
        return st.session_state.get("user_id")
    
    @staticmethod
    def get_token() -> str | None:
        """Obtiene JWT token del usuario actual"""
        return st.session_state.get("token")
    
    @staticmethod
    def require_auth(func):
        """Decorator para requerir autenticación en página"""
        def wrapper(*args, **kwargs):
            if not SessionManager.is_authenticated():
                st.error("❌ Debes iniciar sesión para acceder a esta página")
                st.info("👈 Usa el sidebar para iniciar sesión")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    
    @staticmethod
    def require_role(required_role: str):
        """Decorator para requerir un rol específico"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                user = SessionManager.get_current_user()
                if not user or user.get("role") != required_role:
                    st.error(f"❌ Se requiere rol: {required_role}")
                    st.stop()
                return func(*args, **kwargs)
            return wrapper
        return decorator
