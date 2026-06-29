import streamlit as st
import pandas as pd
from datetime import datetime
from app.utils.logger import logger

def show_annotations_list(annotations: list, current_user_id: int = None):
    """
    Muestra lista de anotaciones de un polígono
    
    Args:
        annotations: Lista de anotaciones (dicts)
        current_user_id: ID del usuario actual para permitir editar
    """
    if not annotations:
        st.info("📭 No hay anotaciones en este polígono")
        return
    
    st.subheader(f"💬 Anotaciones ({len(annotations)})")
    
    # Ordenar por fecha (más reciente primero)
    sorted_annotations = sorted(
        annotations,
        key=lambda x: x.get('created_at', ''),
        reverse=True
    )
    
    for idx, annotation in enumerate(sorted_annotations):
        with st.container():
            # Header de anotación
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                author = annotation.get('author', 'Usuario')
                annotation_type = annotation.get('annotation_type', 'comment')
                type_emoji = {
                    'comment': '💬',
                    'flag': '🚩',
                    'suggestion': '💡',
                    'issue': '⚠️'
                }.get(annotation_type, '📝')
                
                st.markdown(f"**{type_emoji} {author}**")
            
            with col2:
                created_at = annotation.get('created_at', 'desconocida')
                st.caption(f"📅 {created_at}")
            
            with col3:
                is_resolved = annotation.get('is_resolved', False)
                resolved_text = "✅ Resuelta" if is_resolved else "⏳ Abierta"
                st.caption(resolved_text)
            
            # Contenido
            content = annotation.get('content', '')
            st.markdown(f"> {content}")
            
            # Acciones
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(
                    "➕ Responder",
                    key=f"reply_{idx}",
                    use_container_width=True
                ):
                    st.session_state[f"reply_mode_{idx}"] = True
            
            with col2:
                if current_user_id and annotation.get('author_id') == current_user_id:
                    if st.button(
                        "✏️ Editar",
                        key=f"edit_{idx}",
                        use_container_width=True
                    ):
                        st.info("🚧 Edición en desarrollo")
            
            with col3:
                if not annotation.get('is_resolved'):
                    if st.button(
                        "✔️ Resolver",
                        key=f"resolve_{idx}",
                        use_container_width=True
                    ):
                        st.success("Anotación marcada como resuelta")
            
            # Mostrar formulario de respuesta si está activado
            if st.session_state.get(f"reply_mode_{idx}", False):
                show_reply_form(annotation.get('id'), idx)
            
            # Replies
            replies = annotation.get('replies', [])
            if replies:
                show_annotation_replies(replies)
            
            st.divider()


def show_annotation_replies(replies: list):
    """Muestra replies a una anotación"""
    if not replies:
        return
    
    st.markdown(f"##### 🔗 Respuestas ({len(replies)})")
    
    for reply in replies:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                author = reply.get('author', 'Usuario')
                st.markdown(f"**└ {author}**")
            
            with col2:
                created_at = reply.get('created_at', 'desconocida')
                st.caption(f"📅 {created_at}")
            
            content = reply.get('content', '')
            st.markdown(f">> {content}")


def show_reply_form(annotation_id: int, parent_key: int):
    """Muestra formulario para agregar reply"""
    st.markdown("##### ↩️ Escribir respuesta")
    
    reply_content = st.text_area(
        "Tu respuesta",
        placeholder="Escribe tu comentario...",
        height=100,
        key=f"reply_content_{parent_key}"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Enviar respuesta", key=f"send_reply_{parent_key}"):
            if reply_content.strip():
                st.success("✅ Respuesta agregada")
                st.session_state[f"reply_mode_{parent_key}"] = False
                st.rerun()
            else:
                st.error("Por favor, escribe algo")
    
    with col2:
        if st.button("Cancelar", key=f"cancel_reply_{parent_key}"):
            st.session_state[f"reply_mode_{parent_key}"] = False
            st.rerun()


def show_annotation_filters() -> dict:
    """Muestra filtros de anotaciones"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        annotation_type = st.multiselect(
            "Tipo de anotación",
            ["Comentario", "Flag", "Sugerencia", "Issue"],
            default=["Comentario", "Flag", "Sugerencia", "Issue"]
        )
    
    with col2:
        status = st.multiselect(
            "Estado",
            ["Abierta", "Resuelta"],
            default=["Abierta", "Resuelta"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "Ordenar por",
            ["Más reciente", "Más antigua"]
        )
    
    return {
        "annotation_type": annotation_type,
        "status": status,
        "sort_by": sort_by
    }


def filter_annotations(annotations: list, filters: dict) -> list:
    """Filtra anotaciones según criterios"""
    filtered = annotations
    
    # Por tipo
    type_map = {
        "Comentario": "comment",
        "Flag": "flag",
        "Sugerencia": "suggestion",
        "Issue": "issue"
    }
    
    selected_types = [type_map.get(t) for t in filters.get("annotation_type", [])]
    filtered = [a for a in filtered if a.get('annotation_type') in selected_types]
    
    # Por estado
    selected_statuses = filters.get("status", [])
    if "Abierta" not in selected_statuses:
        filtered = [a for a in filtered if a.get('is_resolved')]
    if "Resuelta" not in selected_statuses:
        filtered = [a for a in filtered if not a.get('is_resolved')]
    
    # Ordenar
    sort_by = filters.get("sort_by", "Más reciente")
    reverse = sort_by == "Más reciente"
    filtered = sorted(
        filtered,
        key=lambda x: x.get('created_at', ''),
        reverse=reverse
    )
    
    return filtered


def show_annotation_stats(annotations: list):
    """Muestra estadísticas de anotaciones"""
    if not annotations:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(annotations)
    resolved = len([a for a in annotations if a.get('is_resolved')])
    open_count = total - resolved
    
    with col1:
        st.metric("Total", total)
    
    with col2:
        st.metric("Abiertas", open_count)
    
    with col3:
        st.metric("Resueltas", resolved)
    
    with col4:
        percent_resolved = (resolved / total * 100) if total > 0 else 0
        st.metric("% Resueltas", f"{percent_resolved:.0f}%")
