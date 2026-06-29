import streamlit as st
import pandas as pd

def show_polygon_search_and_filter(all_features: list) -> dict:
    """
    Muestra controles de búsqueda y filtrado
    
    Args:
        all_features: Lista de features del GeoJSON
        
    Returns:
        dict con parámetros de filtrado
    """
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Buscar polígono",
            placeholder="Busca por nombre, ID o propiedad...",
            help="Busca en todas las propiedades"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Ordenar por",
            ["ID", "Nombre"]
        )
    
    with col3:
        sort_order = st.selectbox(
            "Orden",
            ["Ascendente", "Descendente"]
        )
    
    return {
        "search_term": search_term,
        "sort_by": sort_by,
        "sort_order": sort_order
    }


def filter_features(features: list, search_term: str = "", sort_by: str = "ID", sort_order: str = "Ascendente") -> list:
    """
    Filtra y ordena features
    
    Args:
        features: Lista de features
        search_term: Término a buscar
        sort_by: Campo para ordenar
        sort_order: Orden ascendente o descendente
        
    Returns:
        Lista filtrada y ordenada
    """
    filtered = features
    
    # Filtrar por búsqueda
    if search_term:
        search_lower = search_term.lower()
        filtered = [
            f for f in filtered 
            if (search_lower in str(f.get('id', '')).lower() or
                any(search_lower in str(v).lower() for v in f.get('properties', {}).values()))
        ]
    
    # Ordenar
    reverse = sort_order == "Descendente"
    if sort_by == "ID":
        filtered = sorted(filtered, key=lambda x: x.get('id', 0), reverse=reverse)
    
    return filtered


def show_polygons_table(features: list, on_select_callback=None):
    """
    Muestra tabla de polígonos
    
    Args:
        features: Lista de features
        on_select_callback: Callback cuando se selecciona un polígono
    """
    if not features:
        st.info("No hay polígonos para mostrar")
        return
    
    st.subheader(f"📊 Polígonos ({len(features)})")
    
    # Construir datos para tabla
    table_data = []
    for feature in features:
        props = feature.get('properties', {})
        
        row = {
            "ID": feature.get('id', '—'),
            **{k: v[:30] + "..." if isinstance(v, str) and len(str(v)) > 30 else v 
               for k, v in props.items()}
        }
        table_data.append(row)
    
    df = pd.DataFrame(table_data)
    
    # Mostrar tabla
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    st.caption(f"Total: {len(features)} polígonos")


def show_polygon_quick_stats(all_features: list):
    """Muestra estadísticas rápidas de polígonos"""
    if not all_features:
        return
    
    st.markdown("#### 📈 Estadísticas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total", len(all_features))
    
    with col2:
        st.metric("Min ID", min(f.get('id', 0) for f in all_features))
    
    with col3:
        st.metric("Max ID", max(f.get('id', 0) for f in all_features))
    
    with col4:
        # Contar propiedades únicas
        all_props = set()
        for f in all_features:
            all_props.update(f.get('properties', {}).keys())
        st.metric("Propiedades", len(all_props))
