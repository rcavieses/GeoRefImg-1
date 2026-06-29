import streamlit as st
from app.services.drawing_service import DrawingService
from app.utils.logger import logger

def show_drawing_mode_selector():
    """Selector de modo de dibujo"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        draw_new = st.checkbox("🎨 Dibujar Nuevo", value=False)
    
    with col2:
        edit_existing = st.checkbox("✏️ Editar Existente", value=False)
    
    with col3:
        merge_mode = st.checkbox("🔀 Fusionar", value=False)
    
    return {
        "draw_new": draw_new,
        "edit_existing": edit_existing,
        "merge_mode": merge_mode
    }

def show_drawing_instructions():
    """Muestra instrucciones de dibujo"""
    with st.expander("📖 Instrucciones de Dibujo", expanded=False):
        st.markdown("""
        ### Dibujar Nuevo Polígono
        1. Haz click en el botón "Dibujar" en el mapa
        2. Haz click para agregar vértices
        3. Doble-click para terminar
        4. Valida la forma
        5. Guarda el polígono
        
        ### Editar Polígono Existente
        1. Selecciona el polígono en el mapa
        2. Click en "Editar"
        3. Arrastra vértices o agrega nuevos
        4. Valida cambios
        5. Guarda
        
        ### Fusionar Polígonos
        1. Selecciona múltiples polígonos
        2. Click en "Fusionar"
        3. Revisa resultado
        4. Guarda como nuevo
        """)

def show_polygon_drawing_form():
    """Formulario para polígono dibujado"""
    st.subheader("🎨 Nuevo Polígono")
    
    with st.form("polygon_drawing_form"):
        name = st.text_input(
            "Nombre del Polígono",
            placeholder="Ej: Parcela 2024"
        )
        
        description = st.text_area(
            "Descripción",
            placeholder="Observaciones sobre el polígono",
            height=80
        )
        
        # Datos adicionales
        col1, col2 = st.columns(2)
        
        with col1:
            area_hectareas = st.number_input(
                "Área (hectáreas)",
                min_value=0.0,
                step=0.1,
                disabled=True,
                help="Se calcula automáticamente"
            )
        
        with col2:
            vertices = st.number_input(
                "Vértices",
                min_value=3,
                step=1,
                disabled=True,
                help="Número de puntos del polígono"
            )
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submit = st.form_submit_button(
                "💾 Guardar Polígono",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            st.form_submit_button(
                "🔄 Limpiar",
                use_container_width=True
            )
        
        with col3:
            st.form_submit_button(
                "❌ Cancelar",
                use_container_width=True
            )
        
        if submit:
            if name.strip():
                return {
                    "name": name,
                    "description": description,
                    "area_hectareas": area_hectareas
                }
            else:
                st.error("El nombre es requerido")
    
    return None

def show_polygon_editor_controls(selected_polygon_id: int):
    """Controles para editar polígono"""
    st.subheader(f"✏️ Editar Polígono #{selected_polygon_id}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Eliminar Vértice", use_container_width=True):
            st.info("Selecciona un vértice en el mapa")
    
    with col2:
        if st.button("➕ Agregar Vértice", use_container_width=True):
            st.info("Haz click en el lugar para agregar")
    
    with col3:
        if st.button("🔄 Simplificar", use_container_width=True):
            st.success("Polígono simplificado")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Guardar Cambios", use_container_width=True, type="primary"):
            st.success("Cambios guardados")
    
    with col2:
        if st.button("❌ Descartar", use_container_width=True):
            st.info("Cambios descartados")

def show_polygon_merge_controls(selected_ids: list):
    """Controles para fusionar polígonos"""
    if len(selected_ids) < 2:
        st.warning(f"Selecciona al menos 2 polígonos (tienes {len(selected_ids)})")
        return None
    
    st.subheader(f"🔀 Fusionar {len(selected_ids)} Polígonos")
    
    # Info de polígonos a fusionar
    with st.expander("📋 Polígonos Seleccionados"):
        for pid in selected_ids:
            st.caption(f"Polígono #{pid}")
    
    st.divider()
    
    merge_name = st.text_input(
        "Nombre del Polígono Fusionado",
        placeholder="Ej: Parcela Combinada"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔀 Fusionar", use_container_width=True, type="primary"):
            if merge_name.strip():
                st.success(f"Polígonos fusionados: {merge_name}")
                return {"name": merge_name, "ids": selected_ids}
            else:
                st.error("Nombre requerido")
    
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.info("Operación cancelada")
    
    return None

def show_polygon_stats_panel(stats: dict):
    """Muestra estadísticas del polígono"""
    if not stats:
        return
    
    st.markdown("#### 📊 Estadísticas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Área",
            f"{stats.get('area', 0):.4f}°²"
        )
        st.metric(
            "Vértices",
            stats.get('num_vertices', 0)
        )
    
    with col2:
        st.metric(
            "Perímetro",
            f"{stats.get('perimeter', 0):.4f}°"
        )
        centroid = stats.get('centroid', {})
        st.metric(
            "Centro",
            f"({centroid.get('lat', 0):.4f}, {centroid.get('lng', 0):.4f})"
        )
