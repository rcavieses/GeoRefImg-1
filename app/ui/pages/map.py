import streamlit as st
import pandas as pd
from app.ui.session_manager import SessionManager
from app.services.geopackage_service import GeopackageService
from app.ui.components.map_viewer import show_map_viewer, display_map_stats
from app.ui.components.polygon_details import show_polygon_details, show_selected_polygons_list
from app.ui.components.polygon_selector import show_polygon_search_and_filter, filter_features, show_polygons_table, show_polygon_quick_stats

@SessionManager.require_auth
def show_map():
    """Página principal del mapa"""
    user = SessionManager.get_current_user()
    
    st.title("🗺️ Mapa Interactivo de Polígonos")
    st.markdown("Visualiza, selecciona y valida polígonos en el mapa")
    
    # Inicializar session state
    if "gdf" not in st.session_state:
        with st.spinner("📥 Cargando geopackage..."):
            try:
                st.session_state.gdf = GeopackageService.load_geopackage()
                st.session_state.geojson = GeopackageService.to_geojson(st.session_state.gdf)
                st.session_state.bounds = GeopackageService.get_bounds(st.session_state.gdf)
                st.session_state.center = GeopackageService.get_center(st.session_state.bounds)
                st.success(f"✅ Cargados {len(st.session_state.gdf)} polígonos")
            except Exception as e:
                st.error(f"❌ Error cargando geopackage: {e}")
                return
    
    # Estado para polígono seleccionado
    if "selected_polygon_id" not in st.session_state:
        st.session_state.selected_polygon_id = None
    
    if "selected_ids" not in st.session_state:
        st.session_state.selected_ids = []
    
    # Layout principal: Mapa + Sidebar
    col_map, col_sidebar = st.columns([3, 1])
    
    # ===== MAPA =====
    with col_map:
        st.subheader("Mapa Base")
        
        # Mostrar mapa
        map_data = show_map_viewer(
            geojson_data=st.session_state.geojson,
            center=st.session_state.center,
            zoom=10,
            selected_feature_id=st.session_state.selected_polygon_id,
            height=600
        )
        
        # Procesar eventos del mapa
        if map_data and "last_clicked" in map_data:
            # Información del polígono clickeado
            st.session_state.selected_polygon_id = map_data["last_clicked"]["properties"].get("id")
    
    # ===== SIDEBAR =====
    with col_sidebar:
        st.subheader("⚙️ Controles")
        
        # Validación de geometrías
        if st.button("🔍 Validar Geometrías", use_container_width=True):
            validation = GeopackageService.validate_geometries(st.session_state.gdf)
            st.json(validation)
        
        # Info del geopackage
        with st.expander("ℹ️ Información"):
            st.metric("CRS", GeopackageService.get_crs(st.session_state.gdf))
            st.metric("Polígonos", len(st.session_state.gdf))
            
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Latitud: {st.session_state.bounds['miny']:.2f}°")
            with col2:
                st.caption(f"Longitud: {st.session_state.bounds['minx']:.2f}°")
    
    st.markdown("---")
    
    # ===== SECCIÓN DE BÚSQUEDA Y TABLA =====
    st.subheader("🔍 Explorar Polígonos")
    
    # Filtros
    filters = show_polygon_search_and_filter(st.session_state.geojson["features"])
    
    # Aplicar filtros
    filtered_features = filter_features(
        st.session_state.geojson["features"],
        search_term=filters["search_term"],
        sort_by=filters["sort_by"],
        sort_order=filters["sort_order"]
    )
    
    # Mostrar estadísticas
    show_polygon_quick_stats(filtered_features)
    
    # Mostrar tabla
    show_polygons_table(filtered_features)
    
    st.markdown("---")
    
    # ===== DETALLES DEL POLÍGONO SELECCIONADO =====
    if st.session_state.selected_polygon_id is not None:
        selected_polygon = GeopackageService.get_polygon_by_id(
            st.session_state.gdf,
            st.session_state.selected_polygon_id
        )
        
        show_polygon_details(selected_polygon, st.session_state.selected_polygon_id)
    
    st.markdown("---")
    
    # ===== FOOTER =====
    st.caption(f"📍 Sesión de: {user['username']} | {len(st.session_state.geojson['features'])} polígonos disponibles")
