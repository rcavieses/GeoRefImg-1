import streamlit as st

def show_polygon_selector():
    """Componente para seleccionar polígonos"""
    st.subheader("Seleccionar Polígonos")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Buscar polígono por nombre...")
    
    with col2:
        filter_type = st.selectbox(
            "Filtrar por tipo",
            ["Todos", "Geopackage", "Dibujado"]
        )
    
    return search_term, filter_type
