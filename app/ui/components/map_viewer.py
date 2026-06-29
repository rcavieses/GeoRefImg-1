import streamlit as st
import folium
from folium.plugins import Draw, Fullscreen
from streamlit_folium import st_folium
import json

def create_map(center: tuple, zoom: int = 10, geojson_data: dict = None, selected_feature_id: int = None) -> folium.Map:
    """
    Crea mapa Folium con opciones interactivas
    
    Args:
        center: Tupla (lat, lng)
        zoom: Nivel de zoom
        geojson_data: GeoJSON con polígonos
        selected_feature_id: ID del polígono seleccionado (para resaltar)
        
    Returns:
        Mapa Folium
    """
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="OpenStreetMap"
    )
    
    # Agregar GeoJSON si existe
    if geojson_data:
        def style_function(feature):
            is_selected = feature.get('id') == selected_feature_id
            return {
                'fillColor': '#FFA500' if is_selected else '#3388ff',
                'color': '#FF6B00' if is_selected else '#0051ba',
                'weight': 3 if is_selected else 2,
                'opacity': 1,
                'fillOpacity': 0.7 if is_selected else 0.5,
            }
        
        def on_each_feature(feature, layer):
            props = feature['properties']
            html = "<div style='font-size: 12px; width: 200px;'>"
            
            # ID del polígono
            html += f"<b>ID:</b> {feature['id']}<br>"
            
            # Propiedades
            for key, value in props.items():
                if value and key != 'geometry':
                    html += f"<b>{key}:</b> {value}<br>"
            
            html += "</div>"
            layer.popup = folium.Popup(html, max_width=250)
        
        folium.GeoJson(
            geojson_data,
            style_function=style_function,
            onEachFeature=on_each_feature,
            name='Polígonos'
        ).add_to(m)
    
    # Agregar herramientas
    Draw(
        export=True,
        position='topleft',
        draw_options={
            'polyline': False,
            'polygon': True,
            'rectangle': True,
            'circle': False,
            'circlemarker': False,
            'marker': False,
        }
    ).add_to(m)
    
    Fullscreen().add_to(m)
    
    # Layer control
    folium.LayerControl().add_to(m)
    
    return m


def show_map_viewer(geojson_data: dict = None, center: tuple = None, zoom: int = 10, selected_feature_id: int = None, height: int = 500):
    """
    Muestra mapa interactivo en Streamlit
    
    Args:
        geojson_data: GeoJSON con polígonos
        center: Tupla (lat, lng) para centro del mapa
        zoom: Nivel de zoom
        selected_feature_id: ID del polígono a resaltar
        height: Altura del mapa en píxeles
        
    Returns:
        Datos del mapa (clicks, dibujos, etc)
    """
    if center is None:
        center = [24.5, -110.3]  # Centro de Baja California Sur por defecto
    
    m = create_map(center, zoom, geojson_data, selected_feature_id)
    
    # Mostrar mapa y capturar eventos
    map_data = st_folium(m, width=1400, height=height)
    
    return map_data


def display_map_stats(geojson_data: dict, bounds: dict):
    """Muestra estadísticas del mapa"""
    if not geojson_data:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    num_features = len(geojson_data.get('features', []))
    
    with col1:
        st.metric("Polígonos", num_features)
    
    with col2:
        st.metric("Latitud", f"{bounds['miny']:.2f}° a {bounds['maxy']:.2f}°")
    
    with col3:
        st.metric("Longitud", f"{bounds['minx']:.2f}° a {bounds['maxx']:.2f}°")
    
    with col4:
        center_lat = (bounds['miny'] + bounds['maxy']) / 2
        center_lng = (bounds['minx'] + bounds['maxx']) / 2
        st.metric("Centro", f"({center_lat:.2f}, {center_lng:.2f})")
