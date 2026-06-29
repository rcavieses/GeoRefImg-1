import streamlit as st
from app.config import settings
from app.database import init_db

# Configuración página
st.set_page_config(
    page_title=settings.app_name,
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializar BD
init_db()

# Inicializar session state
if "user" not in st.session_state:
    st.session_state.user = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .sidebar .sidebar-content {
        padding: 2rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🗺️ GeoRef Colaborativo")
    st.markdown("---")
    
    if not st.session_state.authenticated:
        st.info("Por favor, inicia sesión para continuar")
        st.markdown("---")
    else:
        st.success(f"Sesión activa: **{st.session_state.user.get('username', 'Usuario')}**")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
        st.markdown("---")
    
    st.markdown("### Información")
    st.markdown(f"Versión: **1.0.0**")
    st.markdown(f"Ambiente: **{settings.app_env}**")

# Contenido principal
if not st.session_state.authenticated:
    st.title("Bienvenido a GeoRef Colaborativo")
    st.markdown("""
        ### Sistema de Validación Colaborativa de Polígonos
        
        Plataforma para visualizar, validar y anotaciones sobre polígonos geoespaciales.
        
        **Características:**
        - 🗺️ Visualización interactiva de polígonos en mapa
        - ✅ Validación colaborativa de geometrías
        - 💬 Sistema de anotaciones y comentarios
        - 🎨 Herramientas para dibujar nuevos polígonos
        - 📊 Dashboard de validaciones y estadísticas
        - 👥 Gestión multi-usuario con roles
        
        **Próximos pasos:**
        1. Crea una cuenta o inicia sesión
        2. Explora el mapa con los polígonos existentes
        3. Valida los polígonos
        4. Agrega tus observaciones
        
        ---
        *Desarrollado con Streamlit, GeoPandas y Azure SQL*
    """)
    
    # TODO: Agregar formularios de login/register aquí
    st.info("🚧 Funcionalidad de autenticación en desarrollo...")
    
else:
    st.title("Dashboard")
    st.info("📍 Sección principal en desarrollo...")

st.markdown("---")
st.markdown("© 2024 GeoRef Colaborativo. Todos los derechos reservados.")
