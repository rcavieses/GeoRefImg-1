# Migración de ODBC a pymssql

**NOTA**: Esta aplicación ahora usa `pymssql` en lugar de ODBC para mejor compatibilidad con Streamlit y otros deployments.

## ✅ Por qué pymssql?

| Aspecto | pymssql | ODBC Driver 17 |
|--------|---------|---|
| **Instalación** | pip install | Requiere driver del sistema |
| **Streamlit Cloud** | ✓ Compatible | ✗ No soportado |
| **Docker** | ✓ Sin config extra | Requiere instalación en Dockerfile |
| **Windows/Mac/Linux** | ✓ Funciona | ✓ Funciona (pero requiere instalación) |
| **Serverless/Contenedores** | ✓ Funciona | Depende de la plataforma |

## 📝 Configuración Anterior (ODBC) - Archivada

Si necesitabas la configuración anterior con ODBC:

### Instalación del ODBC Driver 17

**Windows**:
```bash
# Descargar desde Microsoft:
# https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# O con Chocolatey:
choco install odbc-driver-sql-server
```

**macOS**:
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17 mssql-tools
```

**Linux (Ubuntu/Debian)**:
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo apt-get install msodbcsql17 mssql-tools
```

### Cadena de Conexión ODBC (archivada)
```
mssql+pyodbc://usuario:contraseña@servidor/base-datos
  ?driver=ODBC+Driver+17+for+SQL+Server
  &TrustServerCertificate=yes
  &Encrypt=yes
```

## 🔄 Migración Realizada

✓ Reemplazado `pyodbc` con `pymssql` en `requirements.txt`  
✓ Actualizada URL de conexión en `app/config.py`  
✓ Optimizado pool de conexiones en `app/database.py`  
✓ Actualizado `.env.example`  

## 🚀 Próximos Pasos

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configura `.env`:
   ```bash
   cp .env.example .env
   # Edita con tus credenciales de Azure SQL
   ```

3. Prueba conexión:
   ```bash
   python test_db_connection.py
   ```

Ver `AZURE_SQL_CONFIG.md` para instrucciones completas.
