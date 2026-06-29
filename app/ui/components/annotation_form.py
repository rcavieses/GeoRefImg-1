import streamlit as st

def show_annotation_form():
    """Formulario para agregar anotación"""
    st.subheader("Agregar Anotación")
    
    annotation_type = st.selectbox(
        "Tipo de anotación",
        ["comment", "flag", "suggestion", "issue"]
    )
    
    content = st.text_area("Contenido de la anotación", height=150)
    
    if st.button("Agregar Anotación", use_container_width=True):
        if content:
            return {
                "annotation_type": annotation_type,
                "content": content,
            }
        else:
            st.error("Por favor, escribe contenido para la anotación")
    
    return None
