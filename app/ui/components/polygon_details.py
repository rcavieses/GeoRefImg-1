import streamlit as st
import pandas as pd
from shapely.geometry import shape
from app.services.geopackage_service import GeopackageService

def show_polygon_details(polygon: dict, polygon_id: int):
    """
    Muestra detalles completos de un polígono
    
    Args:
        polygon: dict con datos del polígono
        polygon_id: ID del polígono
    """
    if not polygon:
        st.warning("Selecciona un polígono en el mapa")
        return
    
    st.subheader(f"📍 Detalles del Polígono #{polygon_id}")
    
    # Información básica
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("ID", polygon_id)
    
    with col2:
        props = polygon.get('properties', {})
        st.metric("Propiedades", len(props))
    
    with col3:
        # Calcular área
        try:
            geom = shape(polygon['geometry'])
            area = GeopackageService.calculate_area(geom)
            st.metric("Área", f"{area:,.0f} m²")
        except:
            st.metric("Área", "—")
    
    # Propiedades del polígono
    st.markdown("#### Propiedades")
    
    props = polygon.get('properties', {})
    if props:
        # Mostrar como tabla
        props_list = []
        for key, value in props.items():
            props_list.append({"Campo": key, "Valor": value})
        
        df = pd.DataFrame(props_list)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay propiedades adicionales")
    
    # Información geométrica
    st.markdown("#### Geometría")
    
    try:
        geom = shape(polygon['geometry'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Tipo", geom.geom_type)
        
        with col2:
            bounds = geom.bounds
            st.metric("Bounds", f"({bounds[0]:.2f}, {bounds[1]:.2f})")
        
        with col3:
            st.metric("Válida", "✓ Sí" if geom.is_valid else "✗ No")
        
        # Coordenadas
        if hasattr(geom, 'exterior'):
            coords = list(geom.exterior.coords)
            st.markdown(f"**Vértices:** {len(coords)}")
            
            with st.expander("Ver coordenadas"):
                coords_df = pd.DataFrame(
                    coords,
                    columns=["Longitud", "Latitud"]
                )
                st.dataframe(coords_df, use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error(f"Error procesando geometría: {e}")
    
    # Acciones
    st.markdown("#### Acciones")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Validar", use_container_width=True):
            st.info("🚧 Funcionalidad de validación en desarrollo")
    
    with col2:
        if st.button("💬 Anotar", use_container_width=True):
            st.info("🚧 Funcionalidad de anotación en desarrollo")
    
    with col3:
        if st.button("📋 Copiar ID", use_container_width=True):
            st.success(f"ID copiado: {polygon_id}")


def show_selected_polygons_list(selected_ids: list, all_features: list):
    """Muestra lista de polígonos seleccionados"""
    if not selected_ids:
        st.info("Selecciona polígonos en el mapa")
        return
    
    st.subheader(f"📌 Seleccionados ({len(selected_ids)})")
    
    selected_features = [f for f in all_features if f['id'] in selected_ids]
    
    for feature in selected_features:
        with st.expander(f"Polígono #{feature['id']}", expanded=False):
            props = feature.get('properties', {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"ID: {feature['id']}")
            with col2:
                st.caption(f"Propiedades: {len(props)}")
            
            if props:
                for key, value in props.items():
                    st.caption(f"**{key}:** {value}")
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Validar #{feature['id']}", use_container_width=True, key=f"val_{feature['id']}"):
                    st.info("🚧 Validación en desarrollo")
            with col2:
                if st.button(f"Anotar #{feature['id']}", use_container_width=True, key=f"ann_{feature['id']}"):
                    st.info("🚧 Anotación en desarrollo")
