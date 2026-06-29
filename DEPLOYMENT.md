# Guía de Despliegue - GeoRef Colaborativo

## Opción 1: Streamlit Cloud (Recomendado)

### Requisitos
- Cuenta GitHub con el repositorio
- Cuenta Streamlit Cloud

### Pasos

1. **Crear archivo de secrets**

```bash
mkdir -p ~/.streamlit
cat > ~/.streamlit/secrets.toml << 'EOF'
AZURE_SQL_SERVER = "your-server.database.windows.net"
AZURE_SQL_DATABASE = "georef_db"
AZURE_SQL_USER = "admin"
AZURE_SQL_PASSWORD = "your-password"
JWT_SECRET_KEY = "your-secret-key-min-32-chars"
EOF
```

2. **Push a GitHub**

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

3. **En Streamlit Cloud**

- Ir a https://streamlit.io/cloud
- Click en "New app"
- Seleccionar repositorio y archivo principal
- Configurar secrets en Settings

### Configurar Secrets en Streamlit Cloud

1. En el dashboard de la app, click en "Settings"
2. Click en "Secrets"
3. Copiar contenido de ~/.streamlit/secrets.toml

Variables requeridas:
```
AZURE_SQL_SERVER
AZURE_SQL_DATABASE
AZURE_SQL_USER
AZURE_SQL_PASSWORD
JWT_SECRET_KEY
```

## Opción 2: Docker + Azure Container Instances

### Requisitos
- Docker instalado
- Azure CLI
- Cuenta Azure

### Pasos

```bash
# 1. Build imagen
docker build -t georef:latest .

# 2. Login a Azure
az login

# 3. Crear registry
az acr create --resource-group mygroup --name myregistry --sku Basic

# 4. Push imagen
docker tag georef:latest myregistry.azurecr.io/georef:latest
docker push myregistry.azurecr.io/georef:latest

# 5. Crear container instance
az container create \
  --resource-group mygroup \
  --name georef-app \
  --image myregistry.azurecr.io/georef:latest \
  --ports 8501 \
  --environment-variables \
    AZURE_SQL_SERVER="your-server.database.windows.net" \
    AZURE_SQL_DATABASE="georef_db" \
    AZURE_SQL_USER="admin" \
  --secure-environment-variables \
    AZURE_SQL_PASSWORD="your-password" \
    JWT_SECRET_KEY="your-secret-key"
```

## Opción 3: Despliegue Local

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar .env
cp .env.example .env
# Editar con credenciales reales

# 3. Ejecutar
streamlit run streamlit_app.py
```

## Verificación Post-Despliegue

1. **Acceder a la app**
   - Ir a https://[app-name].streamlit.app

2. **Test de funcionalidades**
   - [ ] Login/Register funciona
   - [ ] Mapa carga polígonos
   - [ ] Puede crear validaciones
   - [ ] Dashboard muestra datos
   - [ ] Anotaciones se guardan

3. **Verificar BD**
   ```bash
   # Conectar a Azure SQL
   sqlcmd -S your-server.database.windows.net -U admin -P "password" -d georef_db
   SELECT COUNT(*) FROM users;
   SELECT COUNT(*) FROM polygons;
   ```

4. **Monitorear logs**
   - En Streamlit Cloud: Settings → Logs
   - En Azure: Container Instances → Logs

## Troubleshooting

### Error: "Cannot connect to database"

```bash
# Verificar connection string
az sql db show --resource-group mygroup --server myserver --name georef_db

# Verificar firewall
az sql server firewall-rule list --resource-group mygroup --server myserver
```

### Error: "Module not found"

```bash
# Actualizar requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### App lenta

- Verificar connection pooling en config.py
- Agregar índices a BD
- Implementar caching con @st.cache_data
- Reducir número de queries

## Performance

### Optimizaciones Implementadas

- Connection pooling: Si (pool_size=10)
- Query caching: Sí (@st.cache_data)
- Índices BD: Sí (ver migrations/001_initial_schema.sql)
- Lazy loading: Sí (componentes)

### Métricas Esperadas

- Load time: < 2 segundos
- Response time API: < 500ms
- DB queries: < 10 por página

## Mantenimiento

### Backups Automáticos

Azure SQL realiza backups automáticos:
- Full backup: Diario
- Transactional log: Cada 5 minutos
- Retención: 35 días

### Updates

```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "deps: update dependencies"
git push
```

### Monitoreo

Configurar alertas en Azure Monitor para:
- CPU usage > 80%
- Memory usage > 80%
- Failed connections > 0
- Long query times > 2s

## Rollback

Si necesitas revertir:

```bash
# Resetear a commit anterior
git revert <commit-hash>
git push

# En Streamlit Cloud se redeploya automáticamente
```

## Seguridad en Producción

### Checklist

- [ ] Cambiar todos los secrets
- [ ] HTTPS habilitado (Streamlit Cloud lo hace)
- [ ] Firewall DB configurado
- [ ] Backups automáticos verificados
- [ ] Logs monitoreados
- [ ] Rate limiting habilitado
- [ ] CORS configurado correctamente

### Secrets Seguros

NO hacer commit de:
- .env (ya en .gitignore)
- secrets.toml (ya en .gitignore)
- API keys
- Contraseñas

Usar Streamlit Secrets para valores sensibles.

## Support & Help

- Documentación Streamlit: https://docs.streamlit.io
- Azure SQL Docs: https://docs.microsoft.com/azure/sql-database
- Proyecto Issues: https://github.com/rcavieses/GeoRefImg/issues
