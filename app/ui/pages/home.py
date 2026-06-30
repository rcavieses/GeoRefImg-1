import streamlit as st
from app.ui.session_manager import SessionManager

@SessionManager.require_auth
def show_home():
    """Página principal con instrucciones"""
    user = SessionManager.get_current_user()

    st.title(f"👋 Bienvenido, {user['first_name'] or user['username']}!")

    # Información del usuario
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**Usuario:** {user['username']}")

    with col2:
        st.info(f"**Email:** {user['email']}")

    with col3:
        role_emoji = "👑" if user['role'] == "admin" else "✓" if user['role'] == "validator" else "👤"
        st.info(f"**Rol:** {role_emoji} {user['role']}")

    st.markdown("---")

    # Instrucciones principales
    st.subheader("📖 Instrucciones de Uso")

    st.markdown("""
    ### 🗺️ Validador de Polígonos Espaciales

    Esta herramienta permite visualizar, validar y anotar polígonos geoespaciales de manera colaborativa.

    #### ¿Cómo usar?

    **1. Acceder al Mapa**
    - Ve a **🗺️ Mapa** en el navegador izquierdo
    - Verás un mapa interactivo con todos los polígonos cargados
    - Puedes hacer zoom in/out para explorar diferentes áreas

    **2. Seleccionar Polígonos**
    - Haz clic en cualquier polígono en el mapa para seleccionarlo
    - Se iluminará en naranja y verás su información en el panel derecho
    - Puedes seleccionar múltiples polígonos haciendo clic en varios

    **3. Validar Polígonos**
    - Una vez seleccionado un polígono, en el panel derecho verás:
      - 📋 **Información detallada**: Nombre, área, región, estado
      - ✅ **Botones de validación**: Aprobar, Rechazar o Revisar
    - Haz clic en el botón correspondiente para registrar tu validación

    **4. Dibujar Nuevos Polígonos**
    - En el panel derecho, sección **Herramientas**
    - Haz clic en ✏️ **Dibujar** para activar modo dibujo
    - Usa las herramientas del mapa para dibujar el nuevo polígono
    - Completa el nombre y justificación del polígono
    - Haz clic en 💾 **Guardar Polígono**

    **5. Hacer Anotaciones Puntuales**
    - En el panel derecho, sección **Anotaciones**
    - Ingresa las coordenadas (latitud/longitud) o usa el mapa
    - Escribe tu anotación (Observación, Problema, Duda, etc.)
    - Haz clic en 📌 **Agregar anotación puntual**

    **6. Unir Polígonos**
    - Selecciona 2 o más polígonos en el mapa
    - En el panel derecho, sección **Herramientas**
    - Verás la opción de **Fusionar**
    - Dale un nombre al nuevo polígono fusionado
    - Haz clic en 🔗 **Fusionar**

    #### 📌 Notas importantes

    - **Modo dibujo**: Mientras activas el modo dibujo, no puedes seleccionar polígonos existentes
    - **Guardado automático**: Las validaciones se guardan automáticamente en la base de datos
    - **Múltiples selecciones**: Puedes trabajar con varios polígonos a la vez
    - **Anotaciones**: Las anotaciones puntuales se agregan directamente sobre el mapa
    """)

    st.markdown("---")

    # Información adicional
    col1, col2 = st.columns(2)

    with col1:
        st.success("""
            ### ✨ Características Principales

            - 📍 Visualización interactiva de polígonos
            - ✅ Validación colaborativa
            - 🗂️ Gestión de información espacial
            - 📝 Anotaciones y comentarios
            - 🔗 Fusión de polígonos
            - 🎨 Herramientas de dibujo
        """)

    with col2:
        st.info("""
            ### 🎯 Tu Rol

            Como **{role}**, tienes permiso para:
            - ✅ Visualizar todos los polígonos
            - ✅ Validar información espacial
            - ✅ Crear anotaciones puntuales
            - ✅ Dibujar nuevos polígonos
            - ✅ Unir polígonos existentes
        """.format(role=user['role'].upper()))

    st.markdown("---")

    st.info("""
        ### 🚀 Comenzar ahora

        ¡Dirígete a la sección **🗺️ Mapa** para comenzar a validar polígonos!
    """)
