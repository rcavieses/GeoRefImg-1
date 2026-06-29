import streamlit as st

def show_auth_form():
    """Formulario de autenticación (login/register)"""
    tab1, tab2 = st.tabs(["🔐 Iniciar Sesión", "✍️ Registrarse"])
    
    with tab1:
        st.subheader("Iniciar Sesión")
        
        username = st.text_input("Usuario", key="login_username")
        password = st.text_input("Contraseña", type="password", key="login_password")
        
        if st.button("Entrar", use_container_width=True):
            if username and password:
                return {
                    "action": "login",
                    "username": username,
                    "password": password,
                }
            else:
                st.error("Por favor, completa todos los campos")
    
    with tab2:
        st.subheader("Crear Cuenta")
        
        reg_username = st.text_input("Usuario", key="reg_username")
        reg_email = st.text_input("Email", key="reg_email")
        reg_first_name = st.text_input("Nombre", key="reg_first_name")
        reg_last_name = st.text_input("Apellido", key="reg_last_name")
        reg_password = st.text_input("Contraseña", type="password", key="reg_password")
        reg_password_confirm = st.text_input("Confirmar Contraseña", type="password", key="reg_password_confirm")
        
        if st.button("Registrarse", use_container_width=True):
            if all([reg_username, reg_email, reg_password, reg_password_confirm]):
                if reg_password != reg_password_confirm:
                    st.error("Las contraseñas no coinciden")
                else:
                    return {
                        "action": "register",
                        "username": reg_username,
                        "email": reg_email,
                        "password": reg_password,
                        "first_name": reg_first_name,
                        "last_name": reg_last_name,
                    }
            else:
                st.error("Por favor, completa todos los campos")
    
    return None
