import streamlit as st
from datetime import datetime
from app.services.polygon_merge_service import PolygonMergeService
from app.services.validation_action_service import ValidationActionService
from app.database import SessionLocal

def show_polygon_validation_panel(polygon: dict, polygon_id: int):
    """Panel de validación y detalles del polígono seleccionado"""
    if not polygon:
        st.info("Selecciona un polígono en el mapa para ver detalles")
        return

    st.subheader(f"📍 Polígono #{polygon_id}")

    # Información general
    props = polygon.get("properties", {})

    col1, col2 = st.columns(2)
    with col1:
        name = props.get("Name", "Sin nombre")
        st.markdown(f"**Nombre:** {name}")

        area = props.get("AreaKm2", "N/A")
        st.markdown(f"**Área (km²):** {area}")

    with col2:
        region = props.get("Region", "N/A")
        st.markdown(f"**Región:** {region}")

        state = props.get("State", "N/A")
        st.markdown(f"**Estado:** {state}")

    # Más propiedades en expander separado (fuera de este)
    with st.expander("📋 Más detalles"):
        for key, value in props.items():
            if key not in ["Name", "AreaKm2", "Region", "State", "geometry"] and value:
                st.caption(f"**{key}:** {value}")

    # Validación
    st.markdown("---")
    st.subheader("✅ Validación")

    col1, col2, col3 = st.columns(3)

    db = SessionLocal()
    user_id = st.session_state.get("user_id")

    with col1:
        if st.button("✅ Aprobar", use_container_width=True, key=f"approve_{polygon_id}"):
            try:
                ValidationActionService.record_validation_action(
                    db=db,
                    polygon_id=polygon_id,
                    user_id=user_id,
                    action="approved"
                )
                st.session_state[f"polygon_{polygon_id}_status"] = "approved"
                st.success("✅ Polígono aprobado")
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                db.close()

    with col2:
        if st.button("❌ Rechazar", use_container_width=True, key=f"reject_{polygon_id}"):
            try:
                ValidationActionService.record_validation_action(
                    db=db,
                    polygon_id=polygon_id,
                    user_id=user_id,
                    action="rejected"
                )
                st.session_state[f"polygon_{polygon_id}_status"] = "rejected"
                st.error("❌ Polígono rechazado")
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                db.close()

    with col3:
        if st.button("🔄 Revisar", use_container_width=True, key=f"review_{polygon_id}"):
            try:
                ValidationActionService.record_validation_action(
                    db=db,
                    polygon_id=polygon_id,
                    user_id=user_id,
                    action="review"
                )
                st.session_state[f"polygon_{polygon_id}_status"] = "review"
                st.warning("🔄 Marcado para revisión")
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                db.close()

    # Opción de unir
    st.markdown("---")
    st.subheader("🔗 Fusionar")

    if st.button("🔗 Unir con otro", use_container_width=True, key=f"merge_{polygon_id}"):
        if len(st.session_state.selected_polygon_ids) < 2:
            st.warning("Necesitas seleccionar al menos 2 polígonos para unir")
        else:
            st.session_state[f"polygon_{polygon_id}_action"] = {
                "action": "merge_initiated",
                "polygon_id": polygon_id,
                "selected_ids": st.session_state.selected_polygon_ids,
                "timestamp": datetime.now().isoformat()
            }
            st.info(f"Polígonos listos para fusionar: {st.session_state.selected_polygon_ids}")

    # Anotaciones generales
    st.markdown("---")
    st.subheader("💬 Anotaciones Generales")

    annotation = st.text_area(
        "Agregar comentario",
        placeholder="Describe problemas o notas sobre este polígono...",
        key=f"annotation_{polygon_id}",
        height=100,
        label_visibility="collapsed"
    )

    if annotation:
        if st.button("💾 Guardar anotación", use_container_width=True, key=f"save_annotation_{polygon_id}"):
            # Guardar anotación en sesión
            if "annotations" not in st.session_state:
                st.session_state.annotations = {}

            st.session_state.annotations[polygon_id] = {
                "text": annotation,
                "timestamp": datetime.now().isoformat(),
                "user_id": st.session_state.get("user_id")
            }
            st.success("Anotación guardada")

    # Mostrar anotaciones anteriores
    if "annotations" in st.session_state and polygon_id in st.session_state.annotations:
        st.divider()
        ann = st.session_state.annotations[polygon_id]
        st.caption(f"Última anotación: {ann.get('timestamp', 'N/A')}")
        st.info(ann.get("text", ""))


def show_selected_polygons_summary():
    """Resumen de polígonos seleccionados para fusión"""
    if not st.session_state.get("selected_polygon_ids"):
        return

    selected = st.session_state.selected_polygon_ids

    with st.expander(f"🔗 Fusionar polígonos ({len(selected)} seleccionados)", expanded=True):
        st.markdown("Polígonos seleccionados para fusión:")
        for pid in selected:
            st.caption(f"• Polígono #{pid}")

        if len(selected) > 1:
            new_name = st.text_input(
                "Nombre para polígono fusionado",
                placeholder="Ej: Área fusionada",
                key="merge_name"
            )

            if st.button("🔗 Fusionar Polígonos", use_container_width=True):
                if new_name.strip():
                    try:
                        # Realizar la fusión
                        gdf = st.session_state.get("gdf")
                        if gdf is not None:
                            merged = PolygonMergeService.merge_polygons(
                                gdf,
                                selected,
                                new_name
                            )

                            st.session_state.merged_polygon = merged
                            st.session_state.selected_polygon_ids = []

                            st.success(f"✅ {len(selected)} polígonos fusionados como '{new_name}'")
                            st.info(f"Polígonos fusionados: {selected}")

                            # Mostrar resultado
                            with st.expander("📊 Detalles de la fusión"):
                                st.json({
                                    "source_polygons": merged["source_polygons"],
                                    "polygon_count": merged["polygon_count"],
                                    "properties": merged["properties"]
                                })
                        else:
                            st.error("GeoDataFrame no cargado")
                    except Exception as e:
                        st.error(f"❌ Error en la fusión: {str(e)}")
                else:
                    st.warning("Ingresa un nombre para el polígono fusionado")
        else:
            st.caption("Selecciona al menos 2 polígonos para fusionar")
