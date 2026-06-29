import streamlit as st

def show_validation_form():
    """Formulario para validar un polígono"""
    st.subheader("Validar Polígono")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status = st.selectbox(
            "Estado de validación",
            ["pending", "approved", "rejected", "needs_revision"]
        )
    
    with col2:
        score = st.slider("Puntuación", 0, 100, 50)
    
    validation_type = st.selectbox(
        "Tipo de validación",
        ["manual", "topology", "accuracy"]
    )
    
    notes = st.text_area("Notas sobre la validación")
    
    if st.button("Guardar Validación", use_container_width=True):
        return {
            "status": status,
            "score": score,
            "validation_type": validation_type,
            "notes": notes,
        }
    
    return None
