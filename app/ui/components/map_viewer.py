import streamlit as st
import pydeck as pdk
import json
import geopandas as gpd
from shapely.geometry import shape


def geojson_to_pydeck_geojson(geojson_data: dict, selected_ids: list = None) -> dict:
    """Convierte GeoJSON a formato Pydeck con colores basados en selección"""
    if selected_ids is None:
        selected_ids = []

    if not geojson_data or 'features' not in geojson_data:
        return geojson_data

    colored_features = []
    for feature in geojson_data.get('features', []):
        feature_id = feature.get('id')
        is_selected = feature_id in selected_ids

        if is_selected:
            feature['properties']['fillColor'] = [255, 165, 0, 200]
            feature['properties']['lineColor'] = [255, 107, 0, 255]
            feature['properties']['lineWidth'] = 3
        else:
            feature['properties']['fillColor'] = [51, 136, 255, 140]
            feature['properties']['lineColor'] = [0, 81, 186, 255]
            feature['properties']['lineWidth'] = 2

        colored_features.append(feature)

    return {
        'type': 'FeatureCollection',
        'features': colored_features
    }


def create_pydeck_map(
    geojson_data: dict,
    center: tuple,
    zoom: int = 10,
    selected_feature_ids: list = None,
    height: int = 500
) -> pdk.Deck:
    """
    Crea un mapa Pydeck con polígonos interactivos

    Args:
        geojson_data: GeoJSON con polígonos
        center: Tupla (lat, lng)
        zoom: Nivel de zoom
        selected_feature_ids: IDs de polígonos seleccionados
        height: Altura del mapa

    Returns:
        Mapa Pydeck
    """
    if selected_feature_ids is None:
        selected_feature_ids = []

    colored_geojson = geojson_to_pydeck_geojson(geojson_data, selected_feature_ids)

    geojson_layer = pdk.Layer(
        'GeoJsonLayer',
        data=colored_geojson,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=False,
        get_fill_color='properties.fillColor',
        get_line_color='properties.lineColor',
        get_line_width='properties.lineWidth',
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=center[0],
        longitude=center[1],
        zoom=zoom,
        pitch=0,
    )

    deck = pdk.Deck(
        layers=[geojson_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v10',
        tooltip={
            'html': '<b>Polígono #{id}</b><br/>Click para seleccionar',
            'style': {
                'backgroundColor': 'steelblue',
                'color': 'white',
                'fontSize': '12px',
                'padding': '8px'
            }
        }
    )

    return deck


def show_map_viewer(
    geojson_data: dict = None,
    center: tuple = None,
    zoom: int = 10,
    selected_feature_ids: list = None,
    height: int = 500,
    key: str = None
):
    """
    Muestra mapa interactivo Pydeck en Streamlit

    Args:
        geojson_data: GeoJSON con polígonos
        center: Tupla (lat, lng)
        zoom: Nivel de zoom
        selected_feature_ids: Lista de IDs seleccionados
        height: Altura del mapa
        key: Clave para el componente

    Returns:
        None (el mapa se renderiza directamente)
    """
    if center is None:
        center = [24.5, -110.3]

    if selected_feature_ids is None:
        selected_feature_ids = []

    deck = create_pydeck_map(geojson_data, center, zoom, selected_feature_ids, height)

    st.pydeck_chart(deck, use_container_width=True, height=height)
