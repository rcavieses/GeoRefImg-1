import streamlit as st
import pandas as pd
from app.ui.session_manager import SessionManager
from app.services.geopackage_service import GeopackageService
from app.services.drawing_service import DrawingService
from app.services.polygon_service import PolygonService
from app.ui.components.map_viewer import show_map_viewer, display_map_stats
from app.ui.components.polygon_details import show_polygon_details, show_selected_polygons_list
from app.ui.components.polygon_selector import show_polygon_search_and_filter, filter_features, show_polygons_table, show_polygon_quick_stats
from app.ui.components.drawing_tools import (
    show_drawing_mode_selector,
    show_drawing_instructions,
    show_polygon_drawing_form,
    show_polygon_editor_controls,
    show_polygon_stats_panel
)
from app.database import SessionLocal

@SessionManager.require_auth
def show_map():
    """Página principal del mapa"""
    user = SessionManager.get_current_user()
    user_id = SessionManager.get_user_id()
    
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
    
    # Estado para polígono seleccionado y modo dibujo
    if "selected_polygon_id" not in st.session_state:
        st.session_state.selected_polygon_id = None

    if "selected_ids" not in st.session_state:
        st.session_state.selected_ids = []

    if "drawing_mode" not in st.session_state:
        st.session_state.drawing_mode = None

    # Tabs principal
    tab_map, tab_draw = st.tabs(["🗺️ Ver", "🎨 Dibujar"])

    # ===== TAB MAPA =====
    with tab_map:
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

    # ===== TAB DIBUJAR =====
    with tab_draw:
        st.subheader("🎨 Herramientas de Dibujo")

        # Instrucciones
        show_drawing_instructions()

        st.divider()

        # Modo de dibujo
        modes = show_drawing_mode_selector()

        st.divider()

        # Formulario según modo
        db = SessionLocal()

        try:
            if modes["draw_new"]:
                st.markdown("### Dibujar Nuevo Polígono")
                st.info("📍 Haz clic en el mapa para agregar puntos. Doble-clic para terminar.")

                form_data = show_polygon_drawing_form()

                if form_data:
                    try:
                        polygon = PolygonService.create_polygon(
                            db=db,
                            name=form_data["name"],
                            geom_wkt="POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))",  # Placeholder
                            created_by=user_id,
                            source_type="drawn"
                        )

                        st.success(f"✅ Polígono #{polygon.id} guardado: {form_data['name']}")
                        st.balloons()

                    except Exception as e:
                        st.error(f"❌ Error: {e}")

            elif modes["edit_existing"]:
                st.markdown("### Editar Polígono")

                polygon_id = st.number_input(
                    "ID del Polígono a Editar",
                    min_value=0,
                    step=1
                )

                if polygon_id > 0:
                    show_polygon_editor_controls(polygon_id)

            elif modes["merge_mode"]:
                st.markdown("### Fusionar Polígonos")

                num_select = st.number_input(
                    "Cuántos polígonos fusionar",
                    min_value=2,
                    max_value=10,
                    value=2
                )

                selected_ids = []
                for i in range(num_select):
                    pid = st.number_input(f"ID Polígono {i+1}", min_value=0, step=1, key=f"merge_{i}")
                    if pid > 0:
                        selected_ids.append(pid)

                if len(selected_ids) >= 2:
                    try:
                        wkt_list = [
                            "POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))"
                            for _ in selected_ids
                        ]

                        merged_wkt = DrawingService.merge_polygons(wkt_list)

                        if merged_wkt:
                            stats = DrawingService.calculate_polygon_stats(merged_wkt)
                            show_polygon_stats_panel(stats)

                            st.divider()

                            merge_name = st.text_input("Nombre del Polígono Fusionado")

                            if st.button("💾 Guardar Fusionado", type="primary"):
                                if merge_name:
                                    polygon = PolygonService.create_polygon(
                                        db=db,
                                        name=merge_name,
                                        geom_wkt=merged_wkt,
                                        created_by=user_id,
                                        source_type="merged"
                                    )

                                    st.success(f"✅ Polígono fusionado: {merge_name}")
                                else:
                                    st.error("Nombre requerido")

                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        finally:
            db.close()

    st.markdown("---")

    # ===== FOOTER =====
    st.caption(f"📍 Sesión de: {user['username']} | {len(st.session_state.geojson['features'])} polígonos disponibles")
