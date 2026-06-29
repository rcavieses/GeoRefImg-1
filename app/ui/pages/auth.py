import streamlit as st
from app.ui.session_manager import SessionManager
from app.utils.validators import validate_password

def show_login():
    """Muestra formulario de login"""
    st.subheader("🔐 Iniciar Sesión")
    
    with st.form("login_form"):
        username = st.text_input(
            "Usuario",
            placeholder="tu_usuario",
            help="Username con el que te registraste"
        )
        password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="••••••••",
            help="Tu contraseña"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submit_btn = st.form_submit_button("🔓 Entrar", use_container_width=True)
        with col2:
            st.form_submit_button("← Volver", use_container_width=True, disabled=True)
        
        if submit_btn:
            if not username or not password:
                st.error("❌ Por favor, completa todos los campos")
            else:
                with st.spinner("Verificando credenciales..."):
                    result = SessionManager.login_user(username, password)
                
                if result["success"]:
                    st.success(f"✅ {result['message']}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")


def show_register():
    """Muestra formulario de registro"""
    st.subheader("✍️ Crear Cuenta")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "Nombre",
                placeholder="Juan",
                help="Tu nombre (opcional)"
            )
        
        with col2:
            last_name = st.text_input(
                "Apellido",
                placeholder="Pérez",
                help="Tu apellido (opcional)"
            )
        
        username = st.text_input(
            "Usuario",
            placeholder="juan_perez",
            help="3-20 caracteres: letras, números, guiones"
        )
        
        email = st.text_input(
            "Correo Electrónico",
            placeholder="juan@example.com",
            help="Dirección de email válida"
        )
        
        password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="••••••••",
            help="Mín 8 caracteres, mayúscula, número"
        )
        
        password_confirm = st.text_input(
            "Confirmar Contraseña",
            type="password",
            placeholder="••••••••",
            help="Repite tu contraseña"
        )
        
        st.markdown("**Requisitos de contraseña:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("✓ Mínimo 8 caracteres")
        with col2:
            st.caption("✓ Una mayúscula")
        with col3:
            st.caption("✓ Un número")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_btn = st.form_submit_button("📝 Registrarse", use_container_width=True)
        with col2:
            st.form_submit_button("← Volver", use_container_width=True, disabled=True)
        
        if submit_btn:
            # Validaciones
            errors = []
            
            if not username:
                errors.append("Usuario es requerido")
            if not email:
                errors.append("Email es requerido")
            if not password:
                errors.append("Contraseña es requerida")
            
            if password != password_confirm:
                errors.append("Las contraseñas no coinciden")
            else:
                is_valid, msg = validate_password(password)
                if not is_valid:
                    errors.append(f"Contraseña débil: {msg}")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                with st.spinner("Registrando usuario..."):
                    result = SessionManager.register_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                
                if result["success"]:
                    st.success(f"✅ {result['message']}")
                    st.info("👈 Ahora inicia sesión con tus credenciales")
                else:
                    st.error(f"❌ {result['message']}")


def show_auth():
    """Página principal de autenticación"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🗺️ GeoRef Colaborativo")
        st.markdown("---")
        
        # Tabs para login y register
        tab1, tab2 = st.tabs(["🔐 Iniciar Sesión", "✍️ Crear Cuenta"])
        
        with tab1:
            show_login()
        
        with tab2:
            show_register()
        
        st.markdown("---")
        st.markdown("""
            ### Bienvenido a GeoRef Colaborativo
            
            **Sistema de validación colaborativa de polígonos geoespaciales**
            
            Características:
            - 🗺️ Visualización interactiva de polígonos en mapa
            - ✅ Validación colaborativa de geometrías
            - 💬 Sistema de anotaciones y comentarios
            - 🎨 Herramientas para dibujar nuevos polígonos
            - 📊 Dashboard de estadísticas
            - 👥 Gestión multi-usuario con roles
        """)
