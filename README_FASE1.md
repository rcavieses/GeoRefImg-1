# GeoRef Colaborativo 🗺️

Sistema de validación colaborativa de polígonos geoespaciales con Streamlit, GeoPandas y Azure SQL.

## Características

- 🗺️ **Visualización Interactiva**: Mapa con Folium para visualizar polígonos desde geopackage
- ✅ **Validación Colaborativa**: Sistema de validación multi-usuario con diferentes roles
- 💬 **Anotaciones**: Comentarios y sugerencias sobre polígonos
- 🎨 **Herramientas de Dibujo**: Crear nuevos polígonos directamente en el mapa
- 📊 **Dashboard**: Estadísticas y reportes de validaciones
- 👥 **Multi-Usuario**: Gestión de usuarios con roles (admin, validator, user)
- 📈 **Auditoría**: Registro completo de cambios

## Stack Tecnológico

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **BD**: Azure SQL Database
- **Geoespacial**: GeoPandas, Shapely, Folium
- **Autenticación**: JWT con PyJWT

## Instalación

### Requisitos Previos

- Python 3.11+
- pip o conda
- Cuenta en Azure SQL (opcional para desarrollo local con SQLite)
- Git

### Setup Local

1. **Clonar repositorio**
   `ash
   git clone <repo-url>
   cd GeoRefImg-Colaborativo
   `

2. **Crear ambiente virtual**
   `ash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   `

3. **Instalar dependencias**
   `ash
   pip install -r requirements.txt
   `

4. **Configurar variables de entorno**
   `ash
   cp .env.example .env
   # Editar .env con tus credenciales de Azure SQL
   `

5. **Ejecutar migraciones de BD (si es necesario)**
   `ash
   # Ejecutar el script SQL en Azure SQL
   # O usar SQLAlchemy:
   python -c "from app.database import init_db; init_db()"
   `

6. **Ejecutar aplicación**
   `ash
   streamlit run streamlit_app.py
   `

La aplicación estará disponible en http://localhost:8501

## Estructura del Proyecto

`
GeoRefImg-Colaborativo/
├── app/
│   ├── models/           # ORM SQLAlchemy
│   ├── services/         # Lógica de negocio
│   ├── utils/            # Utilidades (seguridad, validadores, etc)
│   ├── ui/
│   │   ├── pages/        # Páginas principales de Streamlit
│   │   └── components/   # Componentes reutilizables
│   ├── config.py         # Configuración
│   └── database.py       # Conexión a BD
├── migrations/           # Scripts SQL
├── tests/                # Tests unitarios
├── data/                 # Archivos de datos (geopackage, etc)
├── .streamlit/           # Configuración Streamlit
├── streamlit_app.py      # Punto de entrada
├── requirements.txt      # Dependencias
└── README.md
`

## Uso

### Para Usuarios

1. Registrarse o iniciar sesión
2. Explorar polígonos en el mapa
3. Seleccionar uno o varios polígonos
4. Validar o agregar anotaciones
5. Ver historial de cambios

### Para Administradores

1. Acceder al panel de administración
2. Gestionar usuarios y roles
3. Ver reportes y estadísticas
4. Exportar datos

## Despliegue

### En Streamlit Cloud

1. Push a GitHub
2. Ir a [Streamlit Cloud](https://streamlit.io/cloud)
3. Conectar repositorio
4. Configurar secrets:
   `
   AZURE_SQL_SERVER = your-server.database.windows.net
   AZURE_SQL_DATABASE = your_db
   AZURE_SQL_USER = your_user
   AZURE_SQL_PASSWORD = your_password
   JWT_SECRET_KEY = your-secret-key
   `
5. Deploy automático en cada push a main

### En Azure Container Instances

`ash
docker build -t georef-app .
az acr build --registry <name> --image georef-app:latest .
az container create --resource-group <group> --name georef --image <registry>.azurecr.io/georef-app:latest
`

## Configuración Azure SQL

### Crear servidor y base de datos

`ash
az sql server create --resource-group <group> --name <server> --admin-user <user> --admin-password <password>
az sql db create --resource-group <group> --server <server> --name georef_db --tier Basic
`

### Ejecutar schema inicial

Ejecutar el script migrations/versions/001_initial_schema.sql en Azure SQL.

## Testing

`ash
pytest tests/
`

## Configuración de Desarrollo

### Usar SQLite en lugar de Azure SQL (para desarrollo local)

En pp/config.py, cambiar:
`python
database_url = "sqlite:///./georef.db"  # Local development
`

## Roadmap

- [x] Setup infraestructura base
- [ ] Autenticación y autorización (Fase 2)
- [ ] Carga y visualización geopackage (Fase 3)
- [ ] Sistema de anotaciones (Fase 4)
- [ ] Validaciones (Fase 5)
- [ ] Herramientas de dibujo (Fase 6)
- [ ] Dashboard y reportes (Fase 7)
- [ ] Testing completo (Fase 8)

## Contribuir

Por favor, crea un branch para cada feature:

`ash
git checkout -b feature/nombre-feature
git commit -m "feat: descripción del cambio"
git push origin feature/nombre-feature
`

## Licencia

MIT License - Ver LICENSE file

## Contacto

Para preguntas o problemas, contacta a rcavieses@gmail.com

---

**Versión**: 1.0.0  
**Última actualización**: 2024-06-29
