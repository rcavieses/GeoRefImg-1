import streamlit as st
import folium
from folium.plugins import Draw, Fullscreen
from streamlit_folium import st_folium
import json

def create_map(center: tuple, zoom: int = 10, geojson_data: dict = None, selected_feature_ids: list = None) -> folium.Map:
    """
    Crea mapa Folium con opciones interactivas

    Args:
        center: Tupla (lat, lng)
        zoom: Nivel de zoom
        geojson_data: GeoJSON con polígonos
        selected_feature_ids: Lista de IDs de polígonos seleccionados (para resaltar)

    Returns:
        Mapa Folium
    """
    if selected_feature_ids is None:
        selected_feature_ids = []

    # Bounds del Golfo de California
    # Latitud: 20.59° a 31.86°, Longitud: -114.91° a -105.19°
    min_lat, min_lon = 20.59, -114.91
    max_lat, max_lon = 31.86, -105.19

    gulf_bounds = [[min_lat, min_lon], [max_lat, max_lon]]

    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="OpenStreetMap",
        max_bounds=True
    )

    # Establecer los límites del mapa
    m.fit_bounds(gulf_bounds)

    # Agregar GeoJSON si existe
    if geojson_data:
        def style_function(feature):
            is_selected = feature.get('id') in selected_feature_ids
            return {
                'fillColor': '#FFA500' if is_selected else '#3388ff',
                'color': '#FF6B00' if is_selected else '#0051ba',
                'weight': 3 if is_selected else 2,
                'opacity': 1,
                'fillOpacity': 0.7 if is_selected else 0.5,
            }

        # Agregar cada feature sin popups
        for feature in geojson_data.get('features', []):
            folium.GeoJson(
                feature,
                style_function=style_function,
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


def show_map_viewer(geojson_data: dict = None, center: tuple = None, zoom: int = 10, selected_feature_ids: list = None, height: int = 500, key: str = None):
    """
    Muestra mapa interactivo en Streamlit

    Args:
        geojson_data: GeoJSON con polígonos
        center: Tupla (lat, lng) para centro del mapa
        zoom: Nivel de zoom
        selected_feature_id: ID del polígono a resaltar
        height: Altura del mapa en píxeles
        key: Clave única para el mapa (evita recreaciones innecesarias)

    Returns:
        Datos del mapa (clicks, dibujos, etc)
    """
    if center is None:
        center = [24.5, -110.3]

    if selected_feature_ids is None:
        selected_feature_ids = []

    m = create_map(center, zoom, geojson_data, selected_feature_ids)

    map_data = st_folium(m, width=None, height=height, key=key)

    return map_data


def display_map_stats(geojson_data: dict, bounds: dict):
    """Muestra estadísticas del mapa"""
    if not geojson_data:
        return

    # CSS para reducir tamaño de texto en métricas
    st.markdown("""
        <style>
            [data-testid="metric-container"] {
                font-size: 11px !important;
            }
            [data-testid="metric-container"] [data-testid="stMetricValue"] {
                font-size: 12px !important;
            }
            [data-testid="metric-container"] [data-testid="stMetricLabel"] {
                font-size: 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    num_features = len(geojson_data.get('features', []))

    with col1:
        st.metric("Polígonos", num_features)

    with col2:
        st.metric("Lat", f"{bounds['miny']:.2f}° - {bounds['maxy']:.2f}°")

    with col3:
        st.metric("Lon", f"{bounds['minx']:.2f}° - {bounds['maxx']:.2f}°")

    with col4:
        center_lat = (bounds['miny'] + bounds['maxy']) / 2
        center_lng = (bounds['minx'] + bounds['maxx']) / 2
        st.metric("Centro", f"({center_lat:.1f},{center_lng:.1f})")
