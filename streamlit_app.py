import streamlit as st
from app.config import settings
from app.database import init_db
from app.ui.session_manager import SessionManager
from app.ui.pages import auth, home, map, annotations, validations, dashboard

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
SessionManager.initialize_session()

# CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .sidebar .sidebar-content {
        padding: 2rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.title("🗺️ GeoRef Colaborativo")
    st.markdown("---")

    if SessionManager.is_authenticated():
        # Usuario autenticado
        user = SessionManager.get_current_user()

        # Información del usuario
        col1, col2 = st.columns([3, 1])
        with col1:
            st.success(f"✅ {user['username']}")
        with col2:
            role_emoji = "👑" if user['role'] == "admin" else "✓" if user['role'] == "validator" else "👤"
            st.caption(role_emoji)

        st.markdown("---")

        # Navegación
        st.subheader("🗂️ Navegación")

        pages = {
            "🏠 Inicio": "home",
            "📊 Dashboard": "dashboard",
            "🗺️ Mapa": "map",
            "✅ Validaciones": "validations",
            "💬 Anotaciones": "annotations",
        }

        # Agregar opción admin si es admin
        if user['role'] == "admin":
            pages["👑 Admin"] = "admin"

        current_page = st.radio(
            "Selecciona una sección",
            list(pages.keys()),
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Información del usuario
        with st.expander("👤 Mi Perfil"):
            st.markdown(f"**Usuario:** {user['username']}")
            st.markdown(f"**Email:** {user['email']}")
            st.markdown(f"**Nombre:** {user['first_name'] or '-'} {user['last_name'] or '-'}")
            st.markdown(f"**Rol:** {user['role'].upper()}")

        # Cerrar sesión
        st.markdown("---")
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            SessionManager.logout_user()
            st.success("Sesión cerrada")
            st.rerun()

    else:
        # Usuario no autenticado
        st.info("👤 No estás autenticado")
        st.markdown("---")

    # Footer
    st.markdown("---")
    st.markdown("### ℹ️ Información")
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"Versión: 1.0.0")
    with col2:
        st.caption(f"Ambiente: {settings.app_env}")
    st.caption("© 2024 GeoRef Colaborativo")

# ===== CONTENIDO PRINCIPAL =====

if not SessionManager.is_authenticated():
    # Mostrar página de autenticación
    auth.show_auth()

else:
    # Usuario autenticado - mostrar página solicitada
    user = SessionManager.get_current_user()

    # Obtener página seleccionada del sidebar
    pages = {
        "🏠 Inicio": "home",
        "🗺️ Mapa": "map",
        "✅ Validaciones": "validations",
        "💬 Anotaciones": "annotations",
    }

    if user['role'] == "admin":
        pages["📊 Admin"] = "admin"

    current_page = st.session_state.get("page", "home")

    # Cargar página
    if current_page == "home":
        home.show_home()
    elif current_page == "dashboard":
        dashboard.show_dashboard()
    elif current_page == "map":
        map.show_map()
    elif current_page == "validations":
        validations.show_validations()
    elif current_page == "annotations":
        annotations.show_annotations()
    elif current_page == "admin":
        st.title("👑 Panel de Administración")
        st.info("🚧 Panel admin en desarrollo...")
    else:
        home.show_home()

st.markdown("---")
st.markdown("© 2024 GeoRef Colaborativo. Todos los derechos reservados.")
