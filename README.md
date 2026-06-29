# 🗺️ GeoRef Colaborativo v2

Sistema web de validación colaborativa de polígonos geoespaciales con análisis en tiempo real, anotaciones y control de calidad.

**Migrado de**: GeoRefIMG (aplicación de escritorio)  
**Nueva arquitectura**: Streamlit + Python + Azure SQL  
**Deploy**: Streamlit Cloud  

## 👤 Autor & Desarrollo

**Ricardo Cavieses**  
📧 rcavieses@gmail.com  

**Desarrollo asistido por IA:**
- Claude Haiku 4.5 (Anthropic) - Arquitectura y desarrollo

## 📄 Licencia

**Código Abierto** - MIT License

## 🚀 Características

### **Etapa 1: Georreferenciación**
- ✅ Carga de imágenes PNG
- ✅ Marcado de puntos de control mediante clicks
- ✅ Asignación manual de coordenadas (Longitud/Latitud)
- ✅ Importación de coordenadas desde archivo CSV
- ✅ Cálculo de transformación afín automático
- ✅ Exportación de World File (.pgw)

### **Etapa 2: Digitalización de Polígonos**
- ✅ **Modo líneas**: Clicks para crear líneas rectas conectadas
- ✅ **Modo rectángulo**: Dos clicks para definir esquinas opuestas
- ✅ **Polígonos complejos**: Múltiples anillos/partes por polígono
- ✅ Asignación de nombres a cada polígono
- ✅ Vista previa en tiempo real
- ✅ Exportación a Shapefile (.shp) con campos ID y NAME
- ✅ Exportación de vértices a archivo CSV detallado

## 💿 Instalación y Uso

### **Opción 1: Ejecutable (Recomendado para usuarios finales)**

#### **Descargar y ejecutar:**
1. Descargar el archivo `GeoRefIMG.exe`
2. **No requiere instalación de Python ni dependencias**
3. Hacer doble-click en `GeoRefIMG.exe`
4. La aplicación se abre inmediatamente

#### **Requisitos del sistema:**
- ✅ Windows 7/8/10/11 (32 o 64 bits)
- ✅ Mínimo 4 GB RAM recomendado
- ✅ 150 MB espacio libre en disco
- ✅ **No requiere Python instalado**
- ✅ **No requiere permisos de administrador**

#### **Distribución del ejecutable:**
- **Archivo único**: `GeoRefIMG.exe` (~80-120 MB)
- **Portable**: Se puede ejecutar desde USB, red compartida, etc.
- **Sin instalación**: No modifica el registro de Windows
- **Sin dependencias**: Funciona en computadoras sin Python

#### **Primera ejecución:**
- El primer inicio puede tardar 10-15 segundos (carga librerías embebidas)
- Ejecuciones posteriores son más rápidas
- Si Windows muestra advertencia de "aplicación no reconocida":
  - Click en "Más información"
  - Click en "Ejecutar de todas formas"

### **Opción 2: Código fuente (Para desarrolladores)**

```bash
# Clonar o descargar el proyecto
cd GeoRefIMG

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python georefimg.py
```

### **Opción 3: Crear tu propio ejecutable**

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
pyinstaller --onefile --windowed --name="GeoRefIMG" georefimg.py

# El ejecutable estará en: dist/GeoRefIMG.exe
```

## 📖 Guía de Uso Paso a Paso

### **PASO 1: Cargar Imagen**
1. Abrir `GeoRefIMG.exe`
2. Hacer clic en **"Cargar Imagen"**
3. Seleccionar archivo PNG
4. La imagen aparece en el panel principal

### **PASO 2: Marcar Puntos de Control**
1. Hacer clic en **mínimo 3 puntos** conocidos sobre la imagen
2. Los puntos aparecen como círculos rojos numerados (Punto 1, Punto 2, etc.)
3. Recomendación: Usar esquinas o puntos fácilmente identificables

### **PASO 3: Asignar Coordenadas Reales**

#### **Opción A: Manual**
1. Hacer clic en **"Asignar Coord"**
2. Para cada punto, se abrirán ventanas preguntando:
   - **Longitud** para Punto X: Coordenada Este (ej: -110.3128)
   - **Latitud** para Punto X: Coordenada Norte (ej: 24.1426)

#### **Opción B: Importar CSV**
1. Crear archivo CSV con este formato:
   ```csv
   x,y
   -110.3128,24.1426
   -114.0547,27.9769
   -111.3474,26.0109
   ```
2. Hacer clic en **"Importar CSV"**
3. Seleccionar el archivo CSV
4. Las coordenadas se asignan automáticamente en orden de los puntos clicados

### **PASO 4: Calcular Transformación**
1. Hacer clic en **"Calcular Transform"**
2. Si es exitoso, aparece mensaje: "Transformación calculada correctamente"
3. **Opcional**: Hacer clic en **"Guardar World File"** para exportar archivo .pgw

### **PASO 5: Ir a Digitalización**
1. Hacer clic en **"Ir a Polígonos"**
2. La interfaz cambia al modo de digitalización de polígonos

### **PASO 6: Digitalizar Polígonos**

#### **Modo Líneas (Recomendado para formas irregulares)**
1. Seleccionar radio button **"Líneas"**
2. Hacer clic en **"Empezar Polígono"**
3. Hacer **clicks individuales** en la imagen para crear vértices
4. Las líneas rojas conectan automáticamente los puntos
5. Para finalizar el anillo actual: **"Cerrar Anillo"**
6. Para agregar más partes al mismo polígono: **"Nuevo Anillo"**
7. Para terminar completamente: **"Finalizar Polígono"**
8. Se solicitará un nombre para el polígono

#### **Modo Rectángulo (Para formas regulares)**
1. Seleccionar radio button **"Rectángulo"**  
2. Hacer clic en **"Empezar Polígono"**
3. **Primer click**: Esquina superior izquierda
4. **Segundo click**: Esquina inferior derecha
5. El rectángulo azul se crea automáticamente
6. Se solicitará un nombre para el polígono

### **PASO 7: Gestión de Polígonos**
- **Borrar último**: Elimina el último polígono dibujado
- **Lista de polígonos**: Se muestra en la parte inferior con nombres asignados

### **PASO 8: Exportar Resultados**
1. Hacer clic en **"Exportar Polígonos"**
2. Seleccionar carpeta donde guardar
3. Se crean automáticamente:
   - **poligonos.shp** (+ .shx, .dbf, .prj): Shapefile completo
   - **vertices.csv**: Tabla detallada de vértices

## 🗂️ Formatos de Archivo

### **CSV de Puntos de Control (Entrada)**
```csv
x,y
-110.3128,24.1426
-114.0547,27.9769  
-111.3474,26.0109
```

### **World File (.pgw) - Salida**
```
0.00123456    # Tamaño pixel X
0.0           # Rotación Y  
0.0           # Rotación X
-0.00123456   # Tamaño pixel Y (negativo)
-110.0000     # X esquina superior izquierda
24.5000       # Y esquina superior izquierda
```

### **CSV de Vértices (Salida)**
```csv
poly_id,name,vertex_index,x,y
1,Zona_Urbana,0,-110.3128,24.1426
1,Zona_Urbana,1,-110.3100,24.1400
2,Zona_Industrial,0,-110.2800,24.1200
```

### **Shapefile (Salida)**
- **Campos**: ID (entero), NAME (texto)
- **Geometría**: Polygon (soporta múltiples anillos)
- **Sistema de coordenadas**: WGS84 por defecto

## 🛠️ Dependencias (Solo para código fuente)

```txt
matplotlib>=3.7.0
numpy>=1.24.0
pyshp>=2.3.0
shapely>=2.0.0
imageio>=2.31.0
```

## 💡 Consejos y Mejores Prácticas

### **Selección de Puntos de Control**
- **Mínimo 3 puntos**, recomendado 4-6 para mejor precisión
- **Distribuir** puntos por toda la imagen (no solo en una esquina)
- **Evitar** puntos en línea recta perfecta
- **Usar** intersecciones de calles, esquinas de edificios, etc.

### **Formato de Coordenadas**
- **Longitud (X)**: Negativa para oeste (ej: -110.3128)
- **Latitud (Y)**: Positiva para norte (ej: 24.1426)
- **Precisión**: 4-6 decimales recomendado
- **Sistema**: WGS84 (GPS estándar)

### **Navegación en la Imagen**
- **Zoom**: Rueda del mouse
- **Pan**: Arrastrar con botón derecho del mouse
- **Reset vista**: Doble-click en área vacía

### **Digitalización Eficiente**
- Usar **modo líneas** para límites naturales/irregulares
- Usar **modo rectángulo** para edificios/parcelas regulares
- **Hacer zoom** antes de digitalizar para mayor precisión
- **Nombres descriptivos** para facilitar identificación posterior

## 🌎 Ejemplo de Coordenadas (Baja California Sur, México)

```csv
# Archivo: puntos_control_bcs.csv
x,y
-110.3128,24.1426  # La Paz
-114.0547,27.9769  # Guerrero Negro
-111.3474,26.0109  # Loreto
```

## 🚨 Solución de Problemas

### **El ejecutable no se abre**
- **Verificar**: Windows 7 o superior
- **Descargar**: Microsoft Visual C++ Redistributable más reciente
- **Ejecutar como**: Administrador si persiste el problema

### **Error: "No se puede calcular transformación"**
- **Verificar**: Mínimo 3 puntos marcados
- **Revisar**: Coordenadas correctamente asignadas
- **Evitar**: Puntos en línea recta perfecta

### **Polígonos no se dibujan**
- **Verificar**: Transformación calculada exitosamente
- **Click**: "Empezar Polígono" antes de digitalizar
- **Revisar**: Modo correcto seleccionado (líneas/rectángulo)

### **Ejecutable lento al iniciar**
- **Normal**: Primera carga tarda 10-15 segundos
- **Razón**: Descompresión de librerías embebidas
- **Solución**: Ser paciente, ejecuciones posteriores son rápidas

### **No se exportan los archivos**
- **Verificar**: Permisos de escritura en carpeta destino
- **Verificar**: Espacio suficiente en disco
- **Intentar**: Guardar en otra ubicación (Escritorio, Documentos)

## 📞 Soporte y Contacto

**Dr. Ricardo Cavieses**  
📧 cavieses@uabcs.mx  
🏛️ Universidad Autónoma de Baja California Sur  

Para reportar errores o solicitar mejoras, contactar al autor con:
- Descripción detallada del problema
- Sistema operativo y versión
- Archivos de prueba (si es posible)

## 🤝 Contribuciones

Este es un proyecto de código abierto. Contribuciones, mejoras y sugerencias son bienvenidas.

**Desarrollado con asistencia de IA para la comunidad académica y profesional.**
