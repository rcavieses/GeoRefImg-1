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

    # Inicializar estado de selección
    if "selected_polygon_ids" not in st.session_state:
        st.session_state.selected_polygon_ids = []

    if "annotations" not in st.session_state:
        st.session_state.annotations = {}

    if "last_clicked_id" not in st.session_state:
        st.session_state.last_clicked_id = None

    if "last_click_time" not in st.session_state:
        st.session_state.last_click_time = 0

    if "drawing_mode" not in st.session_state:
        st.session_state.drawing_mode = False

    if "drawn_polygons" not in st.session_state:
        st.session_state.drawn_polygons = []

    if "multi_select_mode" not in st.session_state:
        st.session_state.multi_select_mode = False


    # Layout: Mapa (izquierda) + Panel de control (derecha)
    col_map, col_panel = st.columns([2, 1], gap="small")

    # CSS para hacer más denso el panel derecho
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

    # ===== MAPA PRINCIPAL =====
    with col_map:
        st.subheader("🗺️ Mapa Interactivo")

        # Mostrar mapa
        map_center = (26.0, -111.5)  # Centro de la región Baja California + Golfo
        map_zoom = 7  # Zoom para ver toda la región

        map_data = show_map_viewer(
            geojson_data=st.session_state.geojson,
            center=map_center,
            zoom=map_zoom,
            selected_feature_ids=st.session_state.selected_polygon_ids,
            height=600
        )

        # Procesar clicks en el mapa (solo en modo normal)
        if not st.session_state.drawing_mode:
            if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
                clicked = map_data["last_clicked"]
                lat = clicked.get("lat")
                lng = clicked.get("lng")

                if lat is not None and lng is not None:
                    try:
                        # Buscar qué polígono contiene este punto
                        from shapely.geometry import Point
                        click_point = Point(lng, lat)

                        for idx, row in st.session_state.gdf.iterrows():
                            if row.geometry.contains(click_point):
                                polygon_id = idx
                                if st.session_state.multi_select_mode:
                                    # Modo múltiple: toggle
                                    if polygon_id in st.session_state.selected_polygon_ids:
                                        st.session_state.selected_polygon_ids.remove(polygon_id)
                                    else:
                                        st.session_state.selected_polygon_ids.append(polygon_id)
                                else:
                                    # Modo simple: solo uno a la vez
                                    st.session_state.selected_polygon_ids = [polygon_id]
                                st.rerun()
                                break
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            # En modo dibujo, procesar datos del dibujo
            if map_data and "all_drawings" in map_data:
                drawings = map_data.get("all_drawings", [])
                if drawings:
                    st.session_state.drawn_polygons = drawings

    # ===== PANEL DE CONTROL DERECHO =====
    with col_panel:
        st.subheader("⚙️ Control")

        # Detalles y Validación
        if st.session_state.selected_polygon_ids:
            # Mostrar detalles del primer polígono seleccionado
            selected_id = st.session_state.selected_polygon_ids[0]
            selected_polygon = GeopackageService.get_polygon_by_id(
                st.session_state.gdf,
                selected_id
            )
            show_polygon_validation_panel(
                selected_polygon,
                selected_id
            )

            # Mostrar lista de polígonos seleccionados si hay más de uno y está en modo multi-select
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
                            st.rerun()
        else:
            st.info("👆 Haz clic en un polígono")

        # Herramientas y Selección
        st.divider()
        st.markdown("**🔧 Herramientas**")

        # Selección de polígonos
        st.markdown("**🖱️ Selección**")
        multi_select = st.checkbox(
            "Permitir selección múltiple",
            value=st.session_state.multi_select_mode,
            help="Activa para seleccionar varios polígonos a la vez"
        )
        if multi_select != st.session_state.multi_select_mode:
            st.session_state.multi_select_mode = multi_select
            st.rerun()

        # Modo Dibujo
        st.markdown("**✏️ Modo Dibujo**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Dibujar" if not st.session_state.drawing_mode else "🛑 Detener",
                        use_container_width=True):
                st.session_state.drawing_mode = not st.session_state.drawing_mode
                st.rerun()

        with col2:
            if st.button("🗑️ Limpiar", use_container_width=True):
                st.session_state.drawn_polygons = []
                st.rerun()

        # Mostrar estado
        if st.session_state.drawing_mode:
            st.info("🎨 Modo dibujo activo - seleccionar no funciona")
        else:
            count = len(st.session_state.selected_polygon_ids)
            if count == 0:
                st.caption("0 polígonos seleccionados")
            elif count == 1:
                st.caption("1 polígono seleccionado")
            else:
                st.caption(f"{count} polígonos seleccionados")

        # Guardar polígonos dibujados
        if st.session_state.drawn_polygons:
            st.divider()
            st.markdown("**💾 Guardar Polígono**")

            polygon_name = st.text_input(
                "Nombre del polígono",
                placeholder="Ej: Nueva zona de protección",
                key="new_polygon_name"
            )

            polygon_notes = st.text_area(
                "Justificación/Notas",
                placeholder="¿Por qué se creó este polígono?",
                height=80,
                key="new_polygon_notes"
            )

            if st.button("💾 Guardar Polígono", use_container_width=True):
                if polygon_name.strip() and polygon_notes.strip():
                    try:
                        db = SessionLocal()

                        # Obtener datos del polígono dibujado
                        geojson_data = st.session_state.drawn_polygons[0] if st.session_state.drawn_polygons else None

                        # Guardar en base de datos
                        DrawnPolygonService.create_drawn_polygon(
                            db=db,
                            user_id=user_id,
                            name=polygon_name,
                            justification=polygon_notes,
                            geojson_data=geojson_data
                        )

                        # También guardar en session_state para visualización inmediata
                        if "drawn_polygons" not in st.session_state:
                            st.session_state.drawn_polygons = []

                        st.session_state.drawn_polygons = []
                        st.session_state.drawing_mode = False

                        st.success(f"✅ Polígono '{polygon_name}' guardado en la base de datos")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error guardando polígono: {str(e)}")
                    finally:
                        db.close()
                else:
                    st.warning("⚠️ Completa todos los campos")

        # Mostrar resumen de selección múltiple
        st.divider()
        if st.session_state.selected_polygon_ids:
            show_selected_polygons_summary()
        else:
            if st.button("🔄 Limpiar Selección", use_container_width=True):
                st.session_state.selected_polygon_ids = []

        # Información del mapa
        st.divider()
        if st.button("🔍 Validar Geometrías", use_container_width=True):
            validation = GeopackageService.validate_geometries(st.session_state.gdf)
            st.json(validation)

        with st.expander("ℹ️ Información del Mapa"):
            st.metric("CRS", GeopackageService.get_crs(st.session_state.gdf))
            st.metric("Polígonos", len(st.session_state.gdf))
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Lat: {st.session_state.bounds['miny']:.2f}° a {st.session_state.bounds['maxy']:.2f}°")
            with col2:
                st.caption(f"Lon: {st.session_state.bounds['minx']:.2f}° a {st.session_state.bounds['maxx']:.2f}°")

