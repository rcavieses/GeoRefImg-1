# Guía de Desarrollo - GeoRef Colaborativo

Instrucciones para desarrolladores que quieran contribuir al proyecto.

## Setup de Desarrollo Local

### 1. Clonar y preparar

```bash
git clone <repo>
cd GeoRefImg-Colaborativo

# Crear virtual env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Para desarrollo, instalar dev dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 2. Configurar BD local (SQLite)

Para desarrollo sin Azure:

```bash
# Editar app/config.py
# Cambiar:
# database_url = settings.database_url
# A:
# database_url = "sqlite:///./georef.db"
```

### 3. Ejecutar setup

```bash
python setup.py
```

### 4. Ejecutar app

```bash
streamlit run streamlit_app.py
```

Abre `http://localhost:8501`

## Estructura de Código

### Models (app/models/)

ORM SQLAlchemy - Representan tablas de BD

### Services (app/services/)

Lógica de negocio - No dependen de Streamlit

### UI Components (app/ui/components/)

Widgets reutilizables de Streamlit

### UI Pages (app/ui/pages/)

Páginas completas

### Utils (app/utils/)

Funciones helper sin dependencias Streamlit

## Testing

```bash
# Ejecutar todos los tests
pytest

# Específico
pytest tests/test_mi_feature.py -v

# Con cobertura
pytest --cov=app
```

## Flujo de Desarrollo

1. Crear branch: `git checkout -b feature/nombre`
2. Hacer cambios
3. Escribir tests
4. Ejecutar `pytest`
5. Commit y push
6. Crear PR

## Patrones Comunes

### Proteger página con autenticación

```python
from app.ui.session_manager import SessionManager

@SessionManager.require_auth
def mi_pagina():
    st.title("Página Protegida")

mi_pagina()
```

### Usar servicio

```python
from app.database import SessionLocal
from app.services.user_service import UserService

db = SessionLocal()
try:
    user = UserService.get_user(db, user_id)
finally:
    db.close()
```

### Validaciones

```python
from app.utils.validators import validate_email

if not validate_email(email):
    st.error("Email inválido")
```

## Debug

### Ver estado de sesión

```python
st.write("Session:", st.session_state)
```

### Ver datos usuario

```python
from app.ui.session_manager import SessionManager
st.json(SessionManager.get_current_user())
```

