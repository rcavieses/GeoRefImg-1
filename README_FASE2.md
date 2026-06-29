# Fase 2: Autenticación

Sistema completo de autenticación con login, registro y manejo de sesiones en Streamlit.

## ✅ Qué Incluye Fase 2

### Componentes Nuevos

1. **SessionManager** (`app/ui/session_manager.py`)
   - Gestiona sesiones de usuario
   - Manejo de JWT tokens
   - Decorators para proteger páginas
   
2. **Página de Autenticación** (`app/ui/pages/auth.py`)
   - Formulario de login
   - Formulario de registro con validaciones
   - Interfaz amigable con tabs
   
3. **Página Home** (`app/ui/pages/home.py`)
   - Dashboard post-login
   - Resumen de usuario
   - Quick stats (placeholder)
   
4. **Tests de Autenticación** (`tests/test_auth.py`)
   - Tests registro de usuarios
   - Tests autenticación
   - Tests JWT tokens
   - Tests manejo de errores

### Archivos Actualizados

- `streamlit_app.py` - Integración completa de autenticación
- `.gitignore` - Actualizado para secrets

## 🚀 Usando el Sistema de Autenticación

### Para Usuarios

#### 1. Registrarse

```
- Abre la app
- Click en tab "Crear Cuenta"
- Completa el formulario:
  * Usuario: 3-20 caracteres (letras, números, guiones)
  * Email: válido
  * Nombre y apellido (opcional)
  * Contraseña: mín 8 caracteres, mayúscula, número
- Click en "Registrarse"
```

#### 2. Iniciar Sesión

```
- Click en tab "Iniciar Sesión"
- Ingresa username y contraseña
- Click en "Entrar"
- ¡Listo! Ya estás autenticado
```

#### 3. Navegar (Lado Izquierdo)

```
Una vez autenticado:
- 🏠 Inicio - Dashboard principal
- 🗺️ Mapa - Visualizar polígonos (Fase 3)
- ✅ Validaciones - Validar polígonos (Fase 5)
- 💬 Anotaciones - Ver anotaciones (Fase 4)
- 📊 Admin - Panel admin (si eres admin)
```

#### 4. Cerrar Sesión

```
- Click en "🚪 Cerrar sesión"
- Se limpia la sesión
- Vuelve a página de login
```

### Para Desarrolladores

#### Usar SessionManager en tus páginas

```python
from app.ui.session_manager import SessionManager

# Obtener usuario actual
user = SessionManager.get_current_user()
print(user['username'])  # ej: "juan_perez"

# Obtener ID del usuario
user_id = SessionManager.get_user_id()

# Obtener token JWT
token = SessionManager.get_token()

# Verificar si autenticado
if SessionManager.is_authenticated():
    st.success("Estás autenticado")
```

#### Proteger una página

```python
from app.ui.session_manager import SessionManager

@SessionManager.require_auth
def my_protected_page():
    st.title("Página Protegida")
    st.info("Solo usuarios autenticados pueden ver esto")

my_protected_page()
```

#### Proteger por rol

```python
@SessionManager.require_role("admin")
def admin_only_page():
    st.title("Panel Admin")

admin_only_page()
```

#### Registrar usuario programáticamente

```python
from app.ui.session_manager import SessionManager

result = SessionManager.register_user(
    username="newuser",
    email="new@example.com",
    password="SecurePassword123",
    first_name="Juan",
    last_name="Pérez"
)

if result["success"]:
    print("Usuario registrado:", result["message"])
else:
    print("Error:", result["message"])
```

#### Iniciar sesión programáticamente

```python
result = SessionManager.login_user(
    username="juan",
    password="SecurePassword123"
)

if result["success"]:
    st.success("Logueado")
    user = result["user"]
    print(f"Bienvenido {user['first_name']}")
```

## 🧪 Testing

### Ejecutar todos los tests

```bash
pytest tests/
```

### Ejecutar solo tests de autenticación

```bash
pytest tests/test_auth.py -v
```

### Ejecutar un test específico

```bash
pytest tests/test_auth.py::TestUserAuthentication::test_authenticate_success -v
```

### Con cobertura

```bash
pytest tests/ --cov=app --cov-report=html
```

## 🔐 Seguridad

### Validaciones de Contraseña

Las contraseñas deben cumplir:
- ✅ Mínimo 8 caracteres
- ✅ Al menos una mayúscula
- ✅ Al menos un número

Ejemplo válido: `MyPassword123`

### Validaciones de Username

- ✅ 3-20 caracteres
- ✅ Solo letras, números, guiones
- ✅ No puede haber duplicados

Ejemplo válido: `juan-perez123`

### JWT Tokens

- Se generan con `create_access_token()`
- Expiración configurada en `.env` (default 24 horas)
- Se almacenan en `st.session_state`
- No se envían a cliente (Streamlit maneja server-side)

### Hash de Contraseñas

- Usa bcrypt (implementado en `utils/security.py`)
- Las contraseñas nunca se almacenan en texto plano
- Se verifica con `verify_password()`

## 🐛 Debugging

### Ver estado de sesión

```python
import streamlit as st

st.write("Session State:", st.session_state)
```

### Validar datos de usuario

```python
from app.ui.session_manager import SessionManager

user = SessionManager.get_current_user()
st.json(user)
```

### Ver logs de BD

En `.env`, cambiar:
```
APP_DEBUG=True
```

Luego ejecutar:
```bash
streamlit run streamlit_app.py 2>&1 | grep -i "INSERT\|UPDATE\|SELECT"
```

## 📝 Flujo de Datos

```
┌─────────────────┐
│  Formulario UI  │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│  SessionManager          │
│  - login_user()          │
│  - register_user()       │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  UserService             │
│  - authenticate_user()   │
│  - create_user()         │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Azure SQL Database      │
│  - Tabla: users          │
└──────────────────────────┘
```

## 🚀 Próximo Paso

Fase 3: Cargar geopackage y visualizar polígonos en mapa.

## 📊 Estadísticas

- **Líneas de código agregadas**: ~800
- **Archivos nuevos**: 6
- **Tests**: 13
- **Funcionalidades**: Login, Register, Session management, Role-based access

## ⚠️ Limitaciones Conocidas

- Sin recuperación de contraseña (TODO)
- Sin 2FA (TODO)
- Sin email verification (TODO)
- Sin rate limiting en login (TODO)

## 📚 Referencias

- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [Passlib](https://passlib.readthedocs.io/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
