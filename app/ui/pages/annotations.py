import streamlit as st
import pandas as pd
from app.ui.session_manager import SessionManager
from app.ui.components.annotation_form import show_annotation_form, show_annotation_type_help
from app.ui.components.annotations_list import (
    show_annotations_list,
    show_annotation_filters,
    filter_annotations,
    show_annotation_stats
)
from app.database import SessionLocal
from app.services.annotation_service import AnnotationService
from app.services.polygon_service import PolygonService

@SessionManager.require_auth
def show_annotations():
    """Página principal de anotaciones"""
    user = SessionManager.get_current_user()
    user_id = SessionManager.get_user_id()
    
    st.title("💬 Anotaciones y Comentarios")
    st.markdown("Crea, visualiza y gestiona anotaciones sobre los polígonos")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "➕ Nueva Anotación",
        "📋 Mis Anotaciones",
        "👥 Todas las Anotaciones"
    ])
    
    # ===== TAB 1: NUEVA ANOTACIÓN =====
    with tab1:
        st.subheader("Crear Nueva Anotación")
        
        # Seleccionar polígono
        col1, col2 = st.columns(2)
        
        with col1:
            polygon_id = st.number_input(
                "ID del Polígono",
                min_value=0,
                step=1,
                help="ID del polígono donde deseas anotar"
            )
        
        with col2:
            polygon_name = st.text_input(
                "Nombre/Descripción del Polígono",
                placeholder="Ej: Parcela Sur",
                help="Información adicional (opcional)"
            )
        
        st.divider()
        
        # Formulario
        annotation_data = show_annotation_form(polygon_id)
        
        if annotation_data:
            db = SessionLocal()
            try:
                # Crear anotación
                annotation = AnnotationService.create_annotation(
                    db=db,
                    polygon_id=annotation_data["polygon_id"],
                    author_id=user_id,
                    content=annotation_data["content"],
                    annotation_type=annotation_data["annotation_type"],
                    location=annotation_data.get("location")
                )
                
                st.success(f"✅ Anotación creada: #{annotation.id}")
                st.balloons()
                
                # Mostrar resumen
                with st.expander("📝 Resumen de la anotación"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("ID", annotation.id)
                        st.metric("Tipo", annotation.annotation_type)
                    with col2:
                        st.metric("Autor", user['username'])
                        st.metric("Estado", "Abierta")
                
            except Exception as e:
                st.error(f"❌ Error al crear anotación: {e}")
            finally:
                db.close()
        
        st.divider()
        show_annotation_type_help()
    
    # ===== TAB 2: MIS ANOTACIONES =====
    with tab2:
        st.subheader("Mis Anotaciones")
        
        db = SessionLocal()
        try:
            # Obtener anotaciones del usuario
            # TODO: Implementar query en servicio
            # Por ahora, mostrar placeholder
            
            st.info("🚧 Funcionalidad en desarrollo")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total creadas", "0")
            with col2:
                st.metric("Abiertas", "0")
            with col3:
                st.metric("Resueltas", "0")
            
            st.markdown("---")
            
            # Tabla de anotaciones
            st.subheader("Tus anotaciones recientes")
            
            example_data = {
                "ID": [],
                "Polígono": [],
                "Tipo": [],
                "Contenido": [],
                "Fecha": [],
                "Estado": []
            }
            
            df = pd.DataFrame(example_data)
            if len(df) > 0:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No has creado anotaciones aún")
        
        finally:
            db.close()
    
    # ===== TAB 3: TODAS LAS ANOTACIONES =====
    with tab3:
        st.subheader("Todas las Anotaciones del Sistema")
        
        db = SessionLocal()
        try:
            # Filtros
            col1, col2 = st.columns([3, 1])
            
            with col1:
                search_polygon = st.text_input(
                    "🔍 Buscar por ID de polígono o contenido",
                    placeholder="Ej: 123 o 'límite incorrecto'"
                )
            
            with col2:
                st.markdown("")  # Espaciador
                refresh = st.button("🔄 Actualizar", use_container_width=True)
            
            filters = show_annotation_filters()
            
            st.divider()
            
            # Estadísticas
            # TODO: Implementar queries reales
            
            example_annotations = [
                {
                    "id": 1,
                    "polygon_id": 5,
                    "author": "Juan Pérez",
                    "author_id": 1,
                    "content": "El límite norte parece incorrecto según el shapefile original",
                    "annotation_type": "flag",
                    "created_at": "2024-06-28",
                    "is_resolved": False,
                    "replies": [
                        {
                            "author": "María López",
                            "content": "Confirmado, necesita revisión",
                            "created_at": "2024-06-28"
                        }
                    ]
                },
                {
                    "id": 2,
                    "polygon_id": 12,
                    "author": "Carlos Gómez",
                    "author_id": 3,
                    "content": "Sugerencia: incluir información de elevación",
                    "annotation_type": "suggestion",
                    "created_at": "2024-06-27",
                    "is_resolved": True,
                    "replies": []
                }
            ]
            
            st.subheader("📝 Anotaciones")
            
            # Filtrar
            filtered = filter_annotations(example_annotations, filters)
            
            # Estadísticas
            show_annotation_stats(filtered)
            
            st.divider()
            
            # Listar
            if filtered:
                show_annotations_list(filtered, user_id)
            else:
                st.info("No hay anotaciones que coincidan con los filtros")
        
        finally:
            db.close()
    
    # Footer
    st.markdown("---")
    st.caption(f"👤 Sesión: {user['username']} | 🔐 Rol: {user['role']}")
