# Configuración de Azure SQL con pymssql - Resumen

## ✅ Cambios Realizados

### 1. Dependencias (requirements.txt)
- ✓ `pymssql==2.2.8` - Driver SQL Server para Python (compatible con Streamlit Cloud)
- ✓ `sqlalchemy==2.0.23` - ORM SQL
- ✓ `python-dotenv==1.0.0` - Manejo de variables de entorno

**Nota**: Se reemplazó `pyodbc` con `pymssql` para compatibilidad con Streamlit Cloud.

### 2. Configuración de Base de Datos (`app/config.py`)
- ✓ Parámetros de Azure SQL en la clase `Settings`
- ✓ Cadena de conexión con pymssql:
  ```
  mssql+pymssql://usuario:contraseña@servidor:puerto/base-datos
  ```

### 3. Gestión de Conexiones (`app/database.py`)
- ✓ Pool de conexiones optimizado para Azure SQL
- ✓ Reciclaje de conexiones cada hora (`pool_recycle=3600`)
- ✓ Pool pre-ping para detectar conexiones rotas
- ✓ Modo WAL para SQLite en desarrollo

### 4. Archivos de Configuración
- ✓ `.env.example` - Plantilla con variables necesarias
- ✓ `test_db_connection.py` - Script para verificar conexión

## 🚀 Próximos Pasos

### 1. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales de Azure SQL:

```env
APP_ENV=production

# Datos de Azure SQL
AZURE_SQL_SERVER=tu-servidor.database.windows.net
AZURE_SQL_DATABASE=tu-base-de-datos
AZURE_SQL_USER=tu-usuario@tu-servidor
AZURE_SQL_PASSWORD=tu-contraseña-segura
AZURE_SQL_PORT=1433
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Probar la Conexión

```bash
python test_db_connection.py
```

Deberías ver algo como:
```
🔧 Ambiente: production
📊 Base de datos configurada: mssql+pymssql://usuario...
✅ Conexión exitosa a la base de datos
📌 SQL Server Version: Microsoft SQL Server 2019 ...
```

### 4. Ejecutar Migraciones (si aplica)

```bash
alembic upgrade head
```

## 📋 Entornos

### Desarrollo (APP_ENV=development)
```env
APP_ENV=development
```
- Usa SQLite local (`app.db`)
- No requiere conexión a Azure
- No necesita dependencias especiales

### Producción (APP_ENV=production)
```env
APP_ENV=production
AZURE_SQL_SERVER=...
AZURE_SQL_USER=...
```
- Usa Azure SQL vía pymssql
- Compatible con cualquier plataforma

## 🎯 Ventajas de pymssql

✓ Compatible con Streamlit Cloud  
✓ Sin necesidad de instalar drivers del sistema  
✓ Funciona en Windows, macOS, Linux  
✓ Funciona en Docker sin configuración adicional  
✓ Funciona en contenedores serverless (Azure Functions, etc.)  

## 🔐 Seguridad

- ✓ Las credenciales se cargan desde variables de entorno (`.env`)
- ✓ No incluyas `.env` en el repositorio (está en `.gitignore`)
- ✓ Usa secretos seguros en Azure Key Vault para producción

## 📊 Pool de Conexiones

### Para Azure SQL (pool_size=3, max_overflow=5)
- Máx 3 conexiones simultáneas en el pool
- Permite hasta 5 adicionales temporalmente
- Total máximo: 8 conexiones
- Reciclaje: cada hora

### Para SQLite (NullPool)
- Una conexión por thread
- Sin límites de pool

## 🚀 Deploy en Streamlit Cloud

1. Push tu código a GitHub:
```bash
git add .
git commit -m "Configure Azure SQL with pymssql"
git push
```

2. En https://share.streamlit.io:
   - Click "New app"
   - Conectar tu repositorio GitHub
   - Apuntar a `streamlit_app.py`

3. En "Advanced settings":
   - Añadir Secrets (`.streamlit/secrets.toml`):
   ```toml
   AZURE_SQL_SERVER = "tu-servidor.database.windows.net"
   AZURE_SQL_DATABASE = "tu-base-datos"
   AZURE_SQL_USER = "tu-usuario@tu-servidor"
   AZURE_SQL_PASSWORD = "tu-contraseña"
   AZURE_SQL_PORT = 1433
   APP_ENV = "production"
   ```

## 🔧 Troubleshooting

### Error: "Unknown table 'your_table'"
- Verifica que la base de datos existe
- Ejecuta migraciones: `alembic upgrade head`

### Error: "Login failed"
- Verifica credenciales en `.env` o `secrets.toml`
- Asegúrate que el usuario existe en Azure SQL
- Verifica firewall de Azure SQL (permite Azure Services)

### Error: "Connection timeout"
- Verifica conectividad de red
- Aumenta `login_timeout` en `app/database.py`
- Verifica firewall de Azure SQL

### Error: "charset 'utf8' is not supported"
- En algunos casos, usa `utf-8` en lugar de `utf8`
- Edita `app/database.py` si es necesario

## 📚 Documentación

- [pymssql Documentation](http://www.pymssql.org/)
- [SQLAlchemy - MSSQL Dialect](https://docs.sqlalchemy.org/en/20/dialects/mssql.html)
- [Azure SQL Connection Strings](https://docs.microsoft.com/en-us/azure/azure-sql/database/connect-query-python)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
