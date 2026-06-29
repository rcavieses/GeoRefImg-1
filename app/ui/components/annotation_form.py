import streamlit as st
from datetime import datetime

def show_annotation_form(polygon_id: int = None) -> dict | None:
    """
    Formulario para crear anotación
    
    Args:
        polygon_id: ID del polígono donde anotar
        
    Returns:
        dict con datos de anotación o None si canceló
    """
    st.subheader("✍️ Nueva Anotación")
    
    with st.form("annotation_form", clear_on_submit=True):
        # Tipo de anotación
        annotation_type = st.selectbox(
            "Tipo de anotación",
            [
                ("💬 Comentario", "comment"),
                ("🚩 Flag/Problema", "flag"),
                ("💡 Sugerencia", "suggestion"),
                ("⚠️ Issue/Error", "issue"),
            ],
            format_func=lambda x: x[0]
        )
        annotation_type = annotation_type[1]
        
        # Contenido
        content = st.text_area(
            "Contenido de la anotación",
            placeholder="Escribe tu observación, sugerencia o comentario...",
            height=150,
            max_chars=2000
        )
        
        # Referencia a ubicación (opcional)
        add_location = st.checkbox("Agregar ubicación/coordenadas", value=False)
        
        location = None
        if add_location:
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input(
                    "Latitud",
                    min_value=-90.0,
                    max_value=90.0,
                    step=0.0001,
                    format="%.4f"
                )
            with col2:
                lng = st.number_input(
                    "Longitud",
                    min_value=-180.0,
                    max_value=180.0,
                    step=0.0001,
                    format="%.4f"
                )
            location = {"lat": lat, "lng": lng}
        
        # Botones
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("")  # Espaciador
        
        with col2:
            submit = st.form_submit_button(
                "➕ Agregar Anotación",
                use_container_width=True,
                type="primary"
            )
        
        with col3:
            st.form_submit_button(
                "❌ Cancelar",
                use_container_width=True
            )
        
        # Validar y retornar
        if submit:
            if not content.strip():
                st.error("Por favor, escribe el contenido de la anotación")
            else:
                return {
                    "polygon_id": polygon_id,
                    "content": content.strip(),
                    "annotation_type": annotation_type,
                    "location": location,
                    "created_at": datetime.utcnow().isoformat()
                }
    
    return None


def show_quick_annotation_form(polygon_id: int = None) -> dict | None:
    """
    Formulario comprimido para anotaciones rápidas
    
    Args:
        polygon_id: ID del polígono
        
    Returns:
        dict con datos de anotación o None
    """
    st.markdown("**Anotación Rápida:**")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        content = st.text_input(
            "Escribe tu comentario...",
            placeholder="Ej: Límite incorrecto en el norte",
            label_visibility="collapsed"
        )
    
    with col2:
        submit = st.button("Enviar", use_container_width=True)
    
    if submit and content.strip():
        return {
            "polygon_id": polygon_id,
            "content": content.strip(),
            "annotation_type": "comment",
            "location": None,
            "created_at": datetime.utcnow().isoformat()
        }
    
    return None


def show_annotation_type_help():
    """Muestra ayuda sobre tipos de anotación"""
    with st.expander("ℹ️ Tipos de anotación"):
        st.markdown("""
        - **💬 Comentario:** Observación general o pregunta
        - **🚩 Flag/Problema:** Error o problema detectado
        - **💡 Sugerencia:** Propuesta de mejora
        - **⚠️ Issue/Error:** Error crítico que requiere acción
        """)
