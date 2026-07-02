import streamlit as st
from app.ui.session_manager import SessionManager
from app.services.geopackage_service import GeopackageService
from app.ui.components.map_viewer import show_map_viewer
from app.ui.components.polygon_validation_panel import show_polygon_validation_panel, show_selected_polygons_summary
from app.services.drawn_polygon_service import DrawnPolygonService
from app.database import SessionLocal


@SessionManager.require_auth
def show_map():
    """Página integrada: Mapa + Validación + Anotaciones"""
    user = SessionManager.get_current_user()
    user_id = SessionManager.get_user_id()

    st.title("🗺️ Validador de Polígonos Espaciales")
    st.markdown("Visualiza, valida y anota polígonos directamente en el mapa")

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

    if "selected_polygon_ids" not in st.session_state:
        st.session_state.selected_polygon_ids = []
    if "annotations" not in st.session_state:
        st.session_state.annotations = {}
    if "multi_select_mode" not in st.session_state:
        st.session_state.multi_select_mode = False

    st.markdown("""
        <style>
            .block-container {
                padding-top: 0.5rem;
                padding-bottom: 0.5rem;
            }
            h2 { margin-top: 0.2rem; margin-bottom: 0.2rem; }
            h3 { margin-top: 0.15rem; margin-bottom: 0.15rem; }
            h4 { margin-top: 0.1rem; margin-bottom: 0.1rem; }
            p { margin-top: 0.1rem; margin-bottom: 0.1rem; }
            [data-testid="stMarkdownContainer"] {
                margin-top: 0.1rem;
                margin-bottom: 0.1rem;
            }
            [data-testid="stMetricContainer"] {
                margin-top: 0.1rem;
                margin-bottom: 0.1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1], gap="small")

    # ===== COLUMNA IZQUIERDA: MAPA + HERRAMIENTAS =====
    with col_left:
        st.subheader("🗺️ Mapa Interactivo")

        map_center = (26.0, -111.5)
        map_zoom = 7

        show_map_viewer(
            geojson_data=st.session_state.geojson,
            center=map_center,
            zoom=map_zoom,
            selected_feature_ids=st.session_state.selected_polygon_ids,
            height=500,
            key="main_map"
        )

        # Selector de polígonos
        st.markdown("**🔍 Seleccionar Polígono**")
        col_search, col_list = st.columns([1, 1])

        with col_search:
            search_id = st.text_input(
                "Buscar por ID",
                placeholder="Ej: 1, 2, 3...",
                help="Ingresa el ID del polígono"
            )
            if search_id.strip():
                try:
                    pid = int(search_id.strip())
                    if pid in st.session_state.gdf.index:
                        if st.button("✅ Seleccionar", use_container_width=True):
                            if st.session_state.multi_select_mode:
                                if pid not in st.session_state.selected_polygon_ids:
                                    st.session_state.selected_polygon_ids.append(pid)
                            else:
                                st.session_state.selected_polygon_ids = [pid]
                    else:
                        st.warning(f"⚠️ Polígono #{pid} no existe")
                except ValueError:
                    st.error("❌ Ingresa un número válido")

        with col_list:
            st.markdown("**O elige de la lista:**")
            polygon_options = {f"Polígono #{idx}": idx for idx in st.session_state.gdf.index[:20]}
            selected = st.selectbox(
                "Polígonos disponibles",
                options=list(polygon_options.keys()),
                label_visibility="collapsed"
            )
            if selected:
                pid = polygon_options[selected]
                if st.button("➕ Agregar", use_container_width=True):
                    if st.session_state.multi_select_mode:
                        if pid not in st.session_state.selected_polygon_ids:
                            st.session_state.selected_polygon_ids.append(pid)
                    else:
                        st.session_state.selected_polygon_ids = [pid]

        # ===== HERRAMIENTAS INFERIORES =====
        st.divider()
        st.markdown("**🔧 Herramientas**")

        col_tools1, col_tools2 = st.columns(2)
        with col_tools1:
            st.markdown("**🖱️ Selección**")
            st.session_state.multi_select_mode = st.checkbox(
                "Permitir selección múltiple",
                value=st.session_state.multi_select_mode,
                help="Activa para seleccionar varios polígonos a la vez"
            )

        with col_tools2:
            st.markdown("**📊 Análisis**")
            if st.button("📈 Ver Estadísticas", use_container_width=True):
                st.info("📊 Características del polígono seleccionado")
                if st.session_state.selected_polygon_ids:
                    selected_id = st.session_state.selected_polygon_ids[0]
                    polygon = st.session_state.gdf.iloc[selected_id]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Área", f"{polygon.geometry.area:.2f} m²")
                    with col2:
                        st.metric("Perímetro", f"{polygon.geometry.length:.2f} m")
                else:
                    st.warning("⚠️ Selecciona un polígono primero")

        # Estado de selección
        count = len(st.session_state.selected_polygon_ids)
        if count == 0:
            st.caption("0 polígonos seleccionados")
        elif count == 1:
            st.caption("1 polígono seleccionado")
        else:
            st.caption(f"{count} polígonos seleccionados")

        # Validación y análisis
        st.divider()
        col_val1, col_val2 = st.columns(2)
        with col_val1:
            if st.button("🔍 Validar Geometrías", use_container_width=True):
                validation = GeopackageService.validate_geometries(st.session_state.gdf)
                st.json(validation)

        with col_val2:
            if st.session_state.selected_polygon_ids:
                if st.button("🔄 Limpiar Selección", use_container_width=True):
                    st.session_state.selected_polygon_ids = []

        with st.expander("ℹ️ Información del Mapa"):
            st.metric("CRS", GeopackageService.get_crs(st.session_state.gdf))
            st.metric("Polígonos", len(st.session_state.gdf))
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Lat: {st.session_state.bounds['miny']:.2f}° a {st.session_state.bounds['maxy']:.2f}°")
            with col2:
                st.caption(f"Lon: {st.session_state.bounds['minx']:.2f}° a {st.session_state.bounds['maxx']:.2f}°")

    # ===== COLUMNA DERECHA: INFORMACIÓN DEL POLÍGONO =====
    with col_right:
        st.subheader("📋 Polígono")

        if st.session_state.selected_polygon_ids:
            selected_id = st.session_state.selected_polygon_ids[0]
            selected_polygon = GeopackageService.get_polygon_by_id(
                st.session_state.gdf,
                selected_id
            )
            show_polygon_validation_panel(selected_polygon, selected_id)

            if st.session_state.multi_select_mode and len(st.session_state.selected_polygon_ids) > 1:
                st.divider()
                st.markdown("**Otros seleccionados:**")
                for pid in st.session_state.selected_polygon_ids[1:]:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.caption(f"Polígono #{pid}")
                    with col2:
                        if st.button("❌", key=f"remove_{pid}", use_container_width=True):
                            st.session_state.selected_polygon_ids.remove(pid)

            st.divider()
            show_selected_polygons_summary()
        else:
            st.info("👆 Haz clic en un polígono para ver detalles")
