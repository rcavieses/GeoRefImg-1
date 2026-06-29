# Fase 4: Sistema de Anotaciones y Comentarios

Sistema completo de anotaciones colaborativas con múltiples tipos, respuestas y seguimiento.

## ✅ Qué Incluye Fase 4

### Componentes UI Nuevos

1. **AnnotationsList** (`app/ui/components/annotations_list.py`)
   - Mostrar lista de anotaciones
   - Replies/respuestas
   - Filtros y ordenamiento
   - Estadísticas
   - Marcar como resueltas

2. **AnnotationForm Mejorado** (`app/ui/components/annotation_form.py`)
   - Formulario completo
   - Formulario rápido/comprimido
   - Tipos de anotación con emojis
   - Agregar ubicación/coordenadas
   - Validación de contenido

### Páginas Nuevas

1. **Página de Anotaciones** (`app/ui/pages/annotations.py`)
   - Tab: Nueva anotación
   - Tab: Mis anotaciones
   - Tab: Todas las anotaciones
   - Búsqueda y filtros
   - Integración BD

### Tests

- **test_annotations.py** - 10 tests para anotaciones

## 📝 Características

| Feature | Status | Detalle |
|---------|--------|---------|
| **Crear Anotación** | ✅ | Formulario completo |
| **Tipos** | ✅ | Comment, Flag, Suggestion, Issue |
| **Respuestas** | ✅ | Replies a anotaciones |
| **Búsqueda** | ✅ | Por polígono o contenido |
| **Filtros** | ✅ | Por tipo, estado, ordenamiento |
| **Ubicación** | ✅ | Agregar coordenadas |
| **Resolver** | ✅ | Marcar como resuelta |
| **Estadísticas** | ✅ | Total, abiertas, resueltas |
| **Historial** | ✅ | Timestamps creación/modificación |
| **Colaboración** | ✅ | Multi-usuario |

## 🚀 Cómo Usar

### 1. Crear Anotación

```
Tab "Nueva Anotación":
- Ingresar ID del polígono
- Seleccionar tipo:
  - 💬 Comentario: Observación general
  - 🚩 Flag: Error/Problema
  - 💡 Sugerencia: Propuesta
  - ⚠️ Issue: Error crítico
- Escribir contenido
- (Opcional) Agregar ubicación
- Click "Agregar Anotación"
```

### 2. Ver Mis Anotaciones

```
Tab "Mis Anotaciones":
- Ver todas tus anotaciones creadas
- Filtrar por estado (abierta/resuelta)
- Responder a comentarios
- Editar propias anotaciones
```

### 3. Ver Todas las Anotaciones

```
Tab "Todas las Anotaciones":
- Búsqueda por polígono/contenido
- Filtros avanzados
- Ver respuestas
- Marcar como resuelta
- Estadísticas del sistema
```

## 📋 Tipos de Anotación

### 💬 Comentario
- Observación general
- Pregunta
- Aclaración
- Uso: Cuando quieres hacer un comentario sin urgencia

### 🚩 Flag/Problema
- Error detectado
- Problema en geometría
- Discrepancia de datos
- Uso: Cuando encuentras algo incorrecto

### 💡 Sugerencia
- Propuesta de mejora
- Recomendación
- Optimización
- Uso: Cuando quieres proponer algo

### ⚠️ Issue/Error
- Error crítico
- Requiere acción inmediata
- Problema bloqueante
- Uso: Cuando algo no funciona

## 🔍 API AnnotationService

### Crear anotación

```python
from app.services.annotation_service import AnnotationService
from app.database import SessionLocal

db = SessionLocal()

annotation = AnnotationService.create_annotation(
    db=db,
    polygon_id=123,
    author_id=1,
    content="Límite incorrecto en el norte",
    annotation_type="flag",
    location='{"lat": 24.5, "lng": -110.3}'  # Opcional
)
```

### Obtener anotaciones de un polígono

```python
annotations = AnnotationService.get_annotations(db, polygon_id=123)
for ann in annotations:
    print(f"{ann.author}: {ann.content}")
```

### Obtener anotación específica

```python
annotation = AnnotationService.get_annotation(db, annotation_id=5)
print(annotation.content)
```

### Actualizar anotación

```python
updated = AnnotationService.update_annotation(
    db=db,
    annotation_id=5,
    content="Contenido actualizado",
    is_resolved=True,
    resolved_by=1
)
```

## 🎨 Componentes

### AnnotationsListComponent

```python
from app.ui.components.annotations_list import show_annotations_list

show_annotations_list(
    annotations=annotations_list,
    current_user_id=user_id
)
```

### AnnotationFormComponent

```python
from app.ui.components.annotation_form import show_annotation_form

data = show_annotation_form(polygon_id=123)
if data:
    # Procesar datos
    pass
```

### Filtros

```python
from app.ui.components.annotations_list import (
    show_annotation_filters,
    filter_annotations
)

filters = show_annotation_filters()
filtered = filter_annotations(annotations, filters)
```

## 🧪 Testing

### Ejecutar tests de anotaciones

```bash
pytest tests/test_annotations.py -v
```

### Test específico

```bash
pytest tests/test_annotations.py::TestAnnotationService::test_create_annotation -v
```

### Con cobertura

```bash
pytest tests/test_annotations.py --cov=app.services.annotation_service
```

## 📊 Datos Almacenados

```
Tabla: annotations
- id (PK)
- polygon_id (FK)
- author_id (FK a users)
- content (texto, max 2000 chars)
- annotation_type (comment, flag, suggestion, issue)
- location (JSON: {lat, lng})
- is_resolved (boolean)
- resolved_by (FK a users, nullable)
- resolved_at (datetime, nullable)
- created_at (timestamp)
- updated_at (timestamp)

Tabla: annotation_replies
- id (PK)
- annotation_id (FK)
- author_id (FK a users)
- content (texto)
- created_at (timestamp)
- updated_at (timestamp)
```

## 🔐 Permisos

- **Crear**: Cualquier usuario autenticado
- **Ver**: Cualquier usuario autenticado
- **Editar**: Solo el autor
- **Resolver**: Autor o admin
- **Eliminar**: Soft delete solo para admins

## ⚠️ Limitaciones Conocidas

- Replies solo se muestran en anotaciones existentes (placeholder)
- Edición de anotaciones aún no implementada
- Búsqueda full-text no implementada
- Sin notificaciones para replies
- Sin @ mentions
- Sin archivos adjuntos

## 🚀 Próximo: Fase 5

**Sistema de Validaciones**

- Estados de validación
- Validación automática de topología
- Aprobación/rechazo de polígonos
- Scoring de validación
- Dashboard de validaciones

## 📊 Estadísticas

- **Líneas de código:** ~700
- **Archivos nuevos:** 3
- **Componentes:** 2 (mejorado 1)
- **Tests:** 10
- **Páginas:** 1

## 📚 Referencias

- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Streamlit Forms](https://docs.streamlit.io/library/api-reference/widgets/st.form)
- [JSON en Python](https://docs.python.org/3/library/json.html)

## 💡 Tips

1. **Estructura de respuesta:** Usa JSON para datos complejos en location
2. **Búsqueda:** Implementa full-text search en versión futura
3. **Notificaciones:** Agregar email cuando se responde tu anotación
4. **Moderación:** Admins pueden eliminar anotaciones ofensivas
5. **Estadísticas:** Reportes de anotaciones por usuario/polígono
