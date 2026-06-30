import streamlit as st
from datetime import datetime
from app.services.point_annotation_service import AnnotationService
from app.database import SessionLocal

def show_point_annotation_tool():
    """Herramienta para agregar anotaciones puntuales en el mapa"""
    st.subheader("📍 Anotaciones Puntuales")

    # Inicializar valores en session_state si no existen
    if "annotation_mode" not in st.session_state:
        st.session_state.annotation_mode = False
    if "temp_annotation_lat" not in st.session_state:
        st.session_state.temp_annotation_lat = None
    if "temp_annotation_lon" not in st.session_state:
        st.session_state.temp_annotation_lon = None

    # Toggle para activar modo anotación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📌 Modo Anotación" if not st.session_state.annotation_mode else "🛑 Salir",
                    use_container_width=True):
            st.session_state.annotation_mode = not st.session_state.annotation_mode
            st.rerun()

    with col2:
        if st.button("Limpiar", use_container_width=True):
            st.session_state.annotation_mode = False
            st.session_state.temp_annotation_lat = None
            st.session_state.temp_annotation_lon = None
            st.rerun()

    # Mostrar estado
    if st.session_state.annotation_mode:
        st.info("🎯 Modo anotación activo - Haz clic en el mapa para capturar coordenadas")
    else:
        st.caption("Haz clic en 'Modo Anotación' para comenzar")

    # Mostrar campos de coordenadas si hay capturadas
    if st.session_state.temp_annotation_lat is not None and st.session_state.temp_annotation_lon is not None:
        st.divider()

        lat = st.session_state.temp_annotation_lat
        lon = st.session_state.temp_annotation_lon

        st.caption(f"📍 Coordenadas capturadas: ({lat:.4f}, {lon:.4f})")

        annotation_text = st.text_area(
            "Descripción",
            placeholder="Describe el problema en esta ubicación...",
            height=80,
            key="point_annotation_text",
            label_visibility="collapsed"
        )

        annotation_type = st.selectbox(
            "Tipo",
            ["Observación", "Problema", "Duda", "Corrección requerida"],
            key="point_annotation_type"
        )

        if st.button("💾 Guardar Anotación", use_container_width=True):
            if annotation_text.strip():
                try:
                    db = SessionLocal()

                    # Guardar en base de datos
                    AnnotationService.create_point_annotation(
                        db=db,
                        user_id=st.session_state.get("user_id"),
                        latitude=lat,
                        longitude=lon,
                        annotation_type=annotation_type,
                        description=annotation_text
                    )

                    # También guardar en session_state para visualización inmediata
                    if "point_annotations" not in st.session_state:
                        st.session_state.point_annotations = []

                    annotation = {
                        "id": len(st.session_state.point_annotations),
                        "lat": lat,
                        "lon": lon,
                        "text": annotation_text,
                        "type": annotation_type,
                        "timestamp": datetime.now().isoformat(),
                        "user_id": st.session_state.get("user_id")
                    }

                    st.session_state.point_annotations.append(annotation)
                    st.session_state.annotation_mode = False
                    st.session_state.temp_annotation_lat = None
                    st.session_state.temp_annotation_lon = None

                    st.success(f"✅ Anotación guardada en ({lat:.4f}, {lon:.4f})")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error guardando anotación: {str(e)}")
                finally:
                    db.close()
            else:
                st.warning("Escribe una descripción")


def show_annotation_list():
    """Lista de todas las anotaciones puntuales"""
    if not st.session_state.get("point_annotations"):
        return

    st.markdown("---")
    st.subheader(f"📌 Anotaciones Puntuales ({len(st.session_state.point_annotations)})")

    for i, ann in enumerate(st.session_state.point_annotations):
        with st.expander(f"📍 {ann['type']} - ({ann['lat']:.4f}, {ann['lon']:.4f})"):
            st.markdown(ann["text"])
            st.caption(f"Fecha: {ann['timestamp']}")

            if st.button(
                "🗑️ Eliminar",
                key=f"delete_annotation_{i}",
                use_container_width=True
            ):
                st.session_state.point_annotations.pop(i)
                st.rerun()
