import streamlit as st
import folium
from streamlit_folium import st_folium

def show_map_viewer(geojson_data=None, center=None, zoom=10):
    """Muestra mapa interactivo con Folium"""
    if center is None:
        center = [24.5, -110.3]  # Centro de Baja California Sur por defecto
    
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="OpenStreetMap"
    )
    
    # Agregar GeoJSON si existe
    if geojson_data:
        folium.GeoJson(geojson_data).add_to(m)
    
    # Mostrar mapa y capturar clics
    map_data = st_folium(m, width=1400, height=500)
    
    return map_data
