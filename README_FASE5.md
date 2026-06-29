# Fase 5: Sistema de Validaciones

Sistema completo de validaciones colaborativas con scoring automático, tipos múltiples y dashboard.

## ✅ Qué Incluye Fase 5

### Servicios Nuevos

1. **GeometryService** (`app/services/geometry_service.py`)
   - Validar geometrías WKT
   - Validar topología
   - Detectar auto-intersecciones
   - Verificar overlaps
   - Calcular quality score automático
   - Arreglar geometrías inválidas

2. **ValidationService Mejorado** (`app/services/validation_service.py`)
   - Crear validaciones con scoring
   - Obtener validaciones de polígonos
   - Obtener validaciones de validadores
   - Actualizar estado
   - Aprobar/rechazar
   - Estadísticas y resúmenes
   - Leaderboard de validadores

### Componentes UI

1. **ValidationDashboard** (`app/ui/components/validation_dashboard.py`)
   - Estadísticas en tiempo real
   - Gráficos por estado
   - Progreso de validación
   - Leaderboard de validadores
   - Timeline de actividad

### Páginas Nuevas

1. **Página de Validaciones** (`app/ui/pages/validations.py`)
   - Tab: Por hacer (pendientes)
   - Tab: Validar (formulario)
   - Tab: Dashboard (estadísticas)
   - Integración BD
   - Forms validados

### Tests

- **test_validations.py** - 11 tests para validaciones
- **test_geometry.py** - 6 tests para geometría

## 📋 Características

| Feature | Status | Detalle |
|---------|--------|---------|
| **Crear Validación** | ✅ | Con scoring 0-100 |
| **Estados** | ✅ | pending, approved, rejected, needs_revision |
| **Tipos** | ✅ | topology, accuracy, completeness, manual |
| **Geometría Válida** | ✅ | Validación topológica automática |
| **Quality Score** | ✅ | Score automático basado en geometría |
| **Dashboard** | ✅ | Gráficos y estadísticas |
| **Leaderboard** | ✅ | Ranking de validadores |
| **Resúmenes** | ✅ | Por polígono y global |
| **Filtros** | ✅ | Por estado, tipo, validador |
| **Reportes** | ✅ | Progreso y estadísticas |

## 🚀 Cómo Usar

### 1. Tab "Por Hacer"

Ver polígonos pendientes de validación:
- Lista todos los pendientes
- Ordenados por fecha
- Mostrar información básica

### 2. Tab "Validar"

Realizar una validación:

```
- Ingresar ID del polígono
- Seleccionar tipo de validación:
  - Topología: Validar estructura geométrica
  - Precisión: Evaluar exactitud de límites
  - Completitud: Verificar que está completo
  - Manual: Validación visual
- Seleccionar estado:
  - ✅ Aprobado: Cumple todos los requisitos
  - ❌ Rechazado: Tiene problemas
  - ⚠️ Requiere Revisión: Necesita cambios
  - ⏳ Pendiente: Sin revisar aún
- Ingresar score (0-100)
- Agregar notas
- Enviar
```

### 3. Tab "Dashboard"

Ver estadísticas:
- Total de validaciones
- Distribución por estado
- Score promedio
- Gráficos de progreso
- Ranking de validadores
- Timeline de actividad

## 🔍 GeometryService API

### Validar geometría

```python
from app.services.geometry_service import GeometryService

result = GeometryService.validate_geometry(
    "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
)

# Retorna:
# {
#   "is_valid": True,
#   "geom_type": "Polygon",
#   "is_empty": False,
#   "errors": []
# }
```

### Validar topología

```python
result = GeometryService.validate_topology(geom_wkt)

# Retorna:
# {
#   "is_valid": True,
#   "warnings": [],
#   "errors": []
# }
```

### Calcular quality score

```python
score = GeometryService.calculate_quality_score(geom_wkt)
# Retorna: 0-100
```

### Verificar overlaps

```python
result = GeometryService.check_geometry_overlap(geom1_wkt, geom2_wkt)

# Retorna:
# {
#   "overlaps": False,
#   "intersects": False,
#   "intersection_area": 0
# }
```

## ✅ ValidationService API

### Crear validación

```python
from app.services.validation_service import ValidationService

validation = ValidationService.create_validation(
    db=db,
    polygon_id=123,
    validator_id=user_id,
    status="approved",
    validation_type="topology",
    score=85,
    notes="Geometría válida"
)
```

### Obtener validaciones

```python
# De un polígono
validations = ValidationService.get_validations(db, polygon_id=123)

# De un validador
validations = ValidationService.get_validator_validations(db, user_id)

# Pendientes
pending = ValidationService.get_pending_validations(db, limit=10)
```

### Acciones rápidas

```python
# Aprobar
ValidationService.approve_validation(db, validation_id, notes="Ok")

# Rechazar
ValidationService.reject_validation(db, validation_id, notes="Error")

# Marcar como requiere revisión
ValidationService.mark_needs_revision(db, validation_id)
```

### Estadísticas

```python
# De un polígono
summary = ValidationService.get_polygon_validation_summary(db, polygon_id)

# Global
stats = ValidationService.get_validation_stats(db)

# Retorna:
# {
#   "total": 45,
#   "by_status": {"approved": 30, "rejected": 5, ...},
#   "average_score": 82.5,
#   "approval_rate": 66.7
# }
```

## 📊 Estados de Validación

```
⏳ PENDING (Pendiente)
  - Creada pero no revisada
  - En cola de validación

✅ APPROVED (Aprobado)
  - Cumple todos los requisitos
  - Listo para usar

❌ REJECTED (Rechazado)
  - Tiene problemas críticos
  - No aprobado

⚠️ NEEDS_REVISION (Requiere Revisión)
  - Necesita correcciones
  - En espera de cambios
```

## 📈 Tipos de Validación

```
🔍 TOPOLOGY (Topología)
  - Estructura geométrica válida
  - No auto-intersecciones
  - Anillo cerrado

📐 ACCURACY (Precisión)
  - Límites exactos
  - Coordenadas correctas
  - Alineación con referencia

✅ COMPLETENESS (Completitud)
  - Polígono completo
  - Cobertura total
  - Sin huecos

👁️ MANUAL (Manual)
  - Revisión visual
  - Validación experta
  - Juicio humano
```

## 🧪 Testing

### Ejecutar tests

```bash
pytest tests/test_validations.py -v
pytest tests/test_geometry_service.py -v
```

### Con cobertura

```bash
pytest tests/test_validations.py --cov=app.services.validation_service
```

## 📊 Datos Almacenados

```
Tabla: validations
- id (PK)
- polygon_id (FK)
- validator_id (FK a users)
- status (pending, approved, rejected, needs_revision)
- validation_type (topology, accuracy, completeness, manual)
- score (0-100, nullable)
- notes (texto)
- metadata (JSON, nullable)
- created_at (timestamp)
- updated_at (timestamp)
```

## ⚠️ Limitaciones Conocidas

- Validación topológica automática parcial (mejorable)
- Sin overlapping detection entre polígonos
- Sin asignación automática de validadores
- Sin notificaciones
- Score manual, sin cálculo automático completo
- Sin versiones de validación

## 🚀 Próximo: Fase 6

**Herramientas para Dibujar Polígonos**

- Dibujar nuevos polígonos en el mapa
- Editar polígonos existentes
- Agrupar/separar polígonos
- Exportar polígonos dibujados
- Guardar en BD

## 📊 Estadísticas Fase 5

- **Líneas de código:** 900+
- **Archivos nuevos:** 4
- **Tests:** 17
- **Componentes:** 1
- **Servicios:** 2 mejorados

## 📚 Referencias

- [Shapely Docs](https://shapely.readthedocs.io/)
- [WKT Format](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
- [Plotly Charts](https://plotly.com/python/)

## 💡 Tips

1. **Quality Score:** Implementable automático con análisis más profundo
2. **Overlaps:** Agregar detección de overlaps entre polígonos
3. **Workflow:** Implementar flujo aprobación (draft → review → approved)
4. **Notificaciones:** Alertar validadores de nuevos polígonos
5. **Métricas:** Dashboard con KPIs por validador
