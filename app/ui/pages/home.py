import streamlit as st
from app.ui.session_manager import SessionManager

@SessionManager.require_auth
def show_home():
    """Página principal del dashboard"""
    user = SessionManager.get_current_user()
    
    # Greeting
    st.title(f"👋 Bienvenido, {user['first_name'] or user['username']}!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Usuario:** {user['username']}")
    
    with col2:
        st.info(f"**Email:** {user['email']}")
    
    with col3:
        role_emoji = "👑" if user['role'] == "admin" else "✓" if user['role'] == "validator" else "👤"
        st.info(f"**Rol:** {role_emoji} {user['role']}")
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Resumen Rápido")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Polígonos", "0", "→ 0 nuevos")
    
    with col2:
        st.metric("Validaciones", "0", "→ 0 pendientes")
    
    with col3:
        st.metric("Anotaciones", "0", "→ 0 no resueltas")
    
    with col4:
        st.metric("Mis Contribuciones", "0", "→ Hoy")
    
    st.markdown("---")
    
    # Next steps
    st.subheader("🚀 Próximos Pasos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            ### 🗺️ Explorar Mapa
            Ver los polígonos disponibles en el mapa interactivo
            
            - Visualizar polígonos del geopackage
            - Seleccionar polígonos
            - Ver detalles y propiedades
        """)
        if st.button("Ir al Mapa", use_container_width=True):
            st.info("🚧 Página de mapa en desarrollo")
    
    with col2:
        st.markdown("""
            ### ✅ Validar Polígonos
            Participar en el proceso de validación colaborativa
            
            - Revisar polígonos asignados
            - Aprobar o rechazar geometrías
            - Agregar comentarios detallados
        """)
        if st.button("Validar Ahora", use_container_width=True):
            st.info("🚧 Página de validaciones en desarrollo")
    
    st.markdown("---")
    
    # Additional info
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
            ### ℹ️ Tu Rol
            
            Tienes permiso para:
            - Ver todos los polígonos
            - Crear anotaciones
            - Participar en validaciones
        """)
    
    with col2:
        st.info("""
            ### 📞 Soporte
            
            ¿Necesitas ayuda?
            - Consulta la documentación
            - Contacta al administrador
            - Reporta problemas
        """)
