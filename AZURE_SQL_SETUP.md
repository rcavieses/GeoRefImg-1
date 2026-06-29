# INSTRUCCIONES DE SETUP PARA AZURE SQL

## 1. Crear servidor Azure SQL

### Opción A: Usando Azure CLI

```bash
# Crear grupo de recursos
az group create --name georef-rg --location eastus

# Crear servidor SQL
az sql server create \
  --resource-group georef-rg \
  --name georef-server \
  --admin-user adminuser \
  --admin-password YourPassword123!

# Crear base de datos
az sql db create \
  --resource-group georef-rg \
  --server georef-server \
  --name georef_db \
  --tier Basic \
  --compute-model Serverless
```

### Opción B: Usando Azure Portal

1. Ir a https://portal.azure.com
2. Crear recurso → Base de datos SQL
3. Llenar formulario
4. Esperar a que se cree

## 2. Configurar Firewall

```bash
# Permitir tu IP local
az sql server firewall-rule create \
  --resource-group georef-rg \
  --server georef-server \
  --name AllowLocalMachine \
  --start-ip-address YOUR_IP \
  --end-ip-address YOUR_IP

# Permitir Azure Services
az sql server firewall-rule create \
  --resource-group georef-rg \
  --server georef-server \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

## 3. Obtener Connection String

```bash
# Con Azure CLI
az sql db show-connection-string \
  --server georef-server \
  --name georef_db \
  --client pyodbc
```

O desde Azure Portal:
- Ir a tu BD
- Click en "Connection strings"
- Copiar PyODBC connection string

## 4. Ejecutar Schema

### Opción A: Usando Azure Data Studio

1. Descargar [Azure Data Studio](https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio)
2. Conectar a servidor SQL
3. Abrir y ejecutar: migrations/versions/001_initial_schema.sql

### Opción B: Usando sqlcmd

```bash
sqlcmd -S server.database.windows.net -U user -P password -d database -i migrations/versions/001_initial_schema.sql
```

### Opción C: Automático con Python

```python
from app.database import init_db
init_db()
```

## 5. Configurar .env

Crear archivo `.env` en la raíz del proyecto:

```
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=georef_db
AZURE_SQL_USER=adminuser
AZURE_SQL_PASSWORD=YourPassword123!
AZURE_SQL_PORT=1433

JWT_SECRET_KEY=your-super-secret-key-min-32-characters-long
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

APP_ENV=development
APP_DEBUG=True
```

## 6. Testing de Conexión

```python
from app.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("✅ Conexión exitosa a Azure SQL")
except Exception as e:
    print(f"❌ Error: {e}")
```

## Costos

- **Tier Basic**: ~$5/mes (desarrollo/testing)
- **Tier Standard**: ~$20-40/mes (producción pequeña)
- **Tier Premium**: $200+/mes (producción escalada)

Para desarrollo local, considera usar **SQLite** (gratis, sin red necesaria).

## Cambiar a SQLite en desarrollo

En `app/config.py`:

```python
# En lugar de Azure SQL:
database_url = "sqlite:///./georef.db"
```

## Restaurar Backups

```bash
# Crear backup
az sql db export \
  --resource-group georef-rg \
  --server georef-server \
  --name georef_db \
  --admin-user adminuser \
  --admin-password YourPassword123! \
  --storage-key your-storage-key \
  --storage-uri https://your-storage.blob.core.windows.net/backup.bacpac

# Restaurar
az sql db import \
  --resource-group georef-rg \
  --server georef-server \
  --name georef_db \
  --admin-user adminuser \
  --admin-password YourPassword123! \
  --storage-key your-storage-key \
  --storage-uri https://your-storage.blob.core.windows.net/backup.bacpac
```
