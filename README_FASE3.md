# Fase 3: Mapa Interactivo y Carga de Geopackage

Visualización completa de polígonos en mapa interactivo con búsqueda, filtrado y selección.

## ✅ Qué Incluye Fase 3

### Servicios Nuevos

1. **GeopackageService** (`app/services/geopackage_service.py`)
   - Cargar geopackage (.gpkg)
   - Convertir a GeoJSON
   - Validar geometrías
   - Calcular áreas
   - Buscar polígonos
   - Obtener bounds y center

### Componentes UI Nuevos

1. **MapViewer** (`app/ui/components/map_viewer.py`)
   - Mapa Folium interactivo
   - Herramientas de dibujo
   - Fullscreen mode
   - Resaltado de polígonos seleccionados
   - Layer control

2. **PolygonDetails** (`app/ui/components/polygon_details.py`)
   - Detalles del polígono seleccionado
   - Tabla de propiedades
   - Información geométrica
   - Coordenadas de vértices
   - Botones de acción (validar, anotar)

3. **PolygonSelector** (`app/ui/components/polygon_selector.py`)
   - Búsqueda por término
   - Filtrado y ordenamiento
   - Tabla de polígonos
   - Estadísticas rápidas

### Páginas Nuevas

1. **Página del Mapa** (`app/ui/pages/map.py`)
   - Layout: Mapa + Sidebar + Tabla
   - Carga de geopackage
   - Interacción usuario
   - Integración completa

### Tests

- **test_geopackage_service.py** - 11 tests para geopackage

## 🗺️ Características Implementadas

| Feature | Status | Detalle |
|---------|--------|---------|
| **Cargar Geopackage** | ✅ | Lee .gpkg automáticamente |
| **Mostrar Mapa** | ✅ | Folium con polígonos |
| **Seleccionar Polígonos** | ✅ | Click en mapa |
| **Búsqueda** | ✅ | Por nombre/propiedad |
| **Filtrado** | ✅ | Ordenamiento A-Z |
| **Detalles** | ✅ | Panel lateral completo |
| **Geometría Válida** | ✅ | Validación topológica |
| **Área** | ✅ | Cálculo en m² |
| **Tabla Polígonos** | ✅ | Vista tabular |

## 📁 Archivo Geopackage

Debe estar en: `data/poligonos.gpkg`

Si no existe, la app mostrará error amigable.

### Crear archivo de prueba

```python
import geopandas as gpd
from shapely.geometry import box

# Crear GeoDataFrame
gdf = gpd.GeoDataFrame(
    {
        "name": ["Polygono 1", "Polygono 2"],
        "value": [10, 20],
        "geometry": [
            box(0, 0, 1, 1),
            box(1, 0, 2, 1)
        ]
    },
    crs="EPSG:4326"
)

# Guardar como geopackage
gdf.to_file("data/poligonos.gpkg", driver="GPKG")
```

## 🚀 Cómo Usar

### 1. Iniciar Sesión

- Abre la app
- Login con usuario creado en Fase 2

### 2. Ir al Mapa

- Click en "🗺️ Mapa" en el sidebar
- Espera a que cargue el geopackage

### 3. Explorar

- **Zoom:** Rueda del ratón o botones
- **Desplazar:** Arrastra con el ratón
- **Fullscreen:** Botón en esquina superior derecha

### 4. Seleccionar Polígono

- Click directo en un polígono del mapa
- O busca en la tabla inferior
- Panel lateral muestra detalles

### 5. Ver Detalles

- ID del polígono
- Todas sus propiedades
- Información geométrica
- Lista de coordenadas
- Botones de validación/anotación (en desarrollo)

### 6. Buscar

- Usa buscador "🔍 Buscar polígono"
- Filtra por nombre o propiedad
- Ordena ascendente/descendente

## 🔍 GeopackageService API

### Cargar geopackage

```python
from app.services.geopackage_service import GeopackageService

gdf = GeopackageService.load_geopackage()
# Returns: GeoDataFrame
```

### Convertir a GeoJSON

```python
geojson = GeopackageService.to_geojson(gdf)
# Returns: dict con FeatureCollection
```

### Obtener bounds y center

```python
bounds = GeopackageService.get_bounds(gdf)
# Returns: {"minx": ..., "miny": ..., "maxx": ..., "maxy": ...}

center = GeopackageService.get_center(bounds)
# Returns: (lat, lng)
```

### Obtener polígono por ID

```python
polygon = GeopackageService.get_polygon_by_id(gdf, polygon_id)
# Returns: dict con Feature
```

### Validar geometrías

```python
validation = GeopackageService.validate_geometries(gdf)
# Returns: {"total": ..., "valid": ..., "invalid": ..., "is_all_valid": ...}
```

### Buscar polígonos

```python
filtered = GeopackageService.search_polygons(gdf, "search_term")
# Returns: GeoDataFrame filtrado
```

### Calcular área

```python
area = GeopackageService.calculate_area(geometry)
# Returns: float (m²)
```

## 🎨 Personalización del Mapa

### Cambiar estilos en map_viewer.py

```python
def style_function(feature):
    return {
        'fillColor': '#3388ff',
        'color': '#0051ba',
        'weight': 2,
        'opacity': 1,
        'fillOpacity': 0.5,
    }
```

### Agregar más capas

```python
# En create_map():
folium.TileLayer('CartoDB positron').add_to(m)
```

### Cambiar herramientas de dibujo

```python
Draw(
    draw_options={
        'polyline': False,
        'polygon': True,
        'rectangle': True,
        'circle': False,
    }
).add_to(m)
```

## 🧪 Testing

### Ejecutar tests

```bash
pytest tests/test_geopackage_service.py -v
```

### Ejecutar todos

```bash
pytest tests/ -v --cov
```

## ⚠️ Limitaciones Conocidas

- Solo soporta .gpkg como fuente de polígonos
- Dibujar polígonos en mapa aún no se guarda
- No hay búsqueda geográfica (proximidad)
- No hay filtrado por propiedades específicas

## 🚀 Próximo: Fase 4

**Sistema de Anotaciones**

- Crear anotaciones en polígonos
- Comentarios y respuestas
- Marcar como resueltas
- Historial de anotaciones

## 📊 Estadísticas

- **Líneas de código:** ~600
- **Archivos nuevos:** 5
- **Tests:** 11
- **Componentes:** 3
- **Servicios:** 1

## 📚 Referencias

- [GeoPandas](https://geopandas.org/)
- [Folium](https://folium.readthedocs.io/)
- [Shapely](https://shapely.readthedocs.io/)
- [Streamlit Folium](https://github.com/randyzwitch/streamlit-folium)
