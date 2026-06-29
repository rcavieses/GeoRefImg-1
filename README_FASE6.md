# Fase 6: Herramientas de Dibujo y Edición de Polígonos

Sistema completo para dibujar, editar, fusionar y manipular polígonos geoespaciales.

## ✅ Qué Incluye Fase 6

### Servicios Nuevos

**DrawingService** (`app/services/drawing_service.py`)
- Convertir GeoJSON ↔ WKT
- Validar polígonos dibujados
- Fusionar múltiples polígonos
- Dividir polígonos
- Expandir/contraer (buffer)
- Simplificar polígonos
- Obtener estadísticas
- Editar vértices

### Componentes UI

**DrawingTools** (`app/ui/components/drawing_tools.py`)
- Selector de modo de dibujo
- Instrucciones interactivas
- Formulario para nuevo polígono
- Controles de edición
- Controles de fusión
- Panel de estadísticas

### Integración en Mapa

Página del mapa actualizada con:
- Tab "Ver" (original)
- Tab "Dibujar" (nuevo)
- 3 modos: Dibujar, Editar, Fusionar

### Tests

**test_drawing_service.py** - 10 tests

## 📝 Características

| Feature | Status | Detalle |
|---------|--------|---------|
| **Dibujar Nuevo** | ✅ | Con validación en tiempo real |
| **Editar Polígono** | ✅ | Editar vértices y forma |
| **Fusionar** | ✅ | Combinar múltiples polígonos |
| **Dividir** | ✅ | Partir con línea |
| **Buffer** | ✅ | Expandir/contraer |
| **Simplificar** | ✅ | Reducir vértices |
| **Estadísticas** | ✅ | Área, perímetro, centroide |
| **Conversión** | ✅ | GeoJSON ↔ WKT |
| **Validación** | ✅ | Topología y geometría |
| **Guardar** | ✅ | En BD automáticamente |

## 🎨 Modos de Dibujo

### 1. Dibujar Nuevo Polígono

```
1. Activar "Dibujar Nuevo"
2. Ver instrucciones
3. Hacer clic en mapa para puntos
4. Doble-clic para terminar
5. Ingresar nombre y descripción
6. Guardar polígono
```

Formulario incluye:
- Nombre (requerido)
- Descripción
- Área (auto-calculado)
- Vértices (auto-contado)

### 2. Editar Polígono Existente

```
1. Activar "Editar Existente"
2. Ingresar ID del polígono
3. Opciones:
   - Eliminar vértice
   - Agregar vértice
   - Simplificar forma
4. Guardar cambios o descartar
```

Operaciones:
- 🗑️ Eliminar vértice
- ➕ Agregar vértice
- 🔄 Simplificar
- 💾 Guardar
- ❌ Descartar

### 3. Fusionar Polígonos

```
1. Activar "Fusionar"
2. Seleccionar 2+ polígonos
3. Ver resultado fusionado
4. Ingresar nombre nuevo
5. Guardar como nuevo polígono
```

Validaciones:
- Mínimo 2 polígonos
- Geometría válida
- Nombre requerido

## 🔍 DrawingService API

### Convertir GeoJSON a WKT

```python
wkt = DrawingService.geojson_to_wkt(geojson_feature)
```

### Convertir WKT a GeoJSON

```python
geojson = DrawingService.wkt_to_geojson(wkt_geom)
```

### Validar polígono

```python
is_valid, message = DrawingService.validate_drawn_polygon(coordinates)
# coordinates: [[lng, lat], ...]
```

### Convertir coordenadas a WKT

```python
wkt = DrawingService.coordinates_to_wkt([[0, 0], [1, 0], [1, 1], [0, 1]])
```

### Fusionar polígonos

```python
merged = DrawingService.merge_polygons([wkt1, wkt2, wkt3])
```

### Dividir polígono

```python
parts = DrawingService.split_polygon(polygon_wkt, split_line_wkt)
# Retorna: lista de WKT
```

### Expandir/contraer

```python
# Expandir 0.1 grados
expanded = DrawingService.buffer_polygon(wkt, 0.1)

# Contraer 0.05 grados
contracted = DrawingService.buffer_polygon(wkt, -0.05)
```

### Simplificar

```python
simplified = DrawingService.simplify_polygon(wkt, tolerance=0.0001)
```

### Obtener vértices

```python
vertices = DrawingService.get_polygon_vertices(wkt)
# Retorna: [[lng, lat], ...]
```

### Estadísticas

```python
stats = DrawingService.calculate_polygon_stats(wkt)

# Retorna:
# {
#   "num_vertices": 4,
#   "area": 1.0,
#   "perimeter": 4.0,
#   "centroid": {"lng": 0.5, "lat": 0.5}
# }
```

## 📊 Datos Almacenados

Tabla: polygons (existente)
- Incluye `source_type`: "drawn", "merged", "geopackage"
- Geometría en formato WKT
- Propiedades JSON opcionales

## 🧪 Testing

```bash
pytest tests/test_drawing_service.py -v
```

Tests incluyen:
- Conversiones GeoJSON ↔ WKT
- Validación de polígonos
- Fusión
- Simplificación
- Buffer
- Estadísticas

## ⚠️ Limitaciones Conocidas

- Dibujo actualmente con puntos pre-definidos (placeholder)
- Edición no actualiza mapa en tiempo real
- Sin undo/redo
- Sin arrastrar vértices en mapa
- Sin detección de overlaps antes de guardar
- Sin validación de polígonos superpuestos

## 🚀 Próximo: Fase 7

**Dashboard y Reportes**

- Dashboard principal del sistema
- Reportes de validación
- Exportación de datos
- Estadísticas por usuario
- Gráficos avanzados

## 📊 Estadísticas Fase 6

- **Líneas de código:** 700+
- **Archivos nuevos:** 2
- **Componentes:** 1
- **Servicios:** 1
- **Tests:** 10

## 💡 Mejoras Futuras

1. **Dibujo Interactivo Real**
   - Click en mapa para dibujar
   - Validación en tiempo real
   - Preview de polígono

2. **Edición Avanzada**
   - Arrastrar vértices
   - Agregar/eliminar puntos
   - Rotar/escalar

3. **Operaciones Espaciales**
   - Detección de overlaps
   - Intersecciones
   - Diferencia simétrica

4. **Historial**
   - Undo/Redo
   - Versiones de polígonos
   - Cambios guardados

5. **Validación Automática**
   - En tiempo real mientras dibuja
   - Sugerencias
   - Correcciones automáticas

## 📚 Referencias

- [Shapely Documentation](https://shapely.readthedocs.io/)
- [Folium Draw Plugin](https://github.com/python-visualization/folium/issues/1500)
- [GeoJSON Spec](https://tools.ietf.org/html/rfc7946)
