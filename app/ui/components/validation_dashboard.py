import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def show_validation_stats(stats: dict):
    """Muestra estadísticas de validación"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Validaciones",
            stats.get("total", 0),
            help="Todas las validaciones realizadas"
        )
    
    with col2:
        approved = stats.get("by_status", {}).get("approved", 0)
        st.metric(
            "Aprobadas",
            approved,
            delta=f"{stats.get('approval_rate', 0):.1f}%"
        )
    
    with col3:
        pending = stats.get("by_status", {}).get("pending", 0)
        st.metric(
            "Pendientes",
            pending,
            delta_color="off"
        )
    
    with col4:
        avg_score = stats.get("average_score", 0)
        st.metric(
            "Score Promedio",
            f"{avg_score:.1f}",
            help="Promedio de scores 0-100"
        )


def show_validation_chart(stats: dict):
    """Muestra gráfico de validaciones por estado"""
    by_status = stats.get("by_status", {})
    
    if not by_status:
        st.info("No hay datos de validación")
        return
    
    # Preparar datos
    labels = list(by_status.keys())
    values = list(by_status.values())
    
    # Colores por estado
    color_map = {
        "pending": "#FFA500",
        "approved": "#28a745",
        "rejected": "#dc3545",
        "needs_revision": "#ffc107"
    }
    
    colors = [color_map.get(label, "#6c757d") for label in labels]
    
    # Crear gráfico
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>%{value} (%{percent})<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Distribución de Validaciones por Estado",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_validation_progress(polygon_summary: dict):
    """Muestra progreso de validación de un polígono"""
    st.subheader("📊 Progreso de Validación")
    
    total = polygon_summary.get("total", 0)
    
    if total == 0:
        st.info("Sin validaciones")
        return
    
    by_status = polygon_summary.get("by_status", {})
    
    # Barra de progreso
    col1, col2 = st.columns([3, 1])
    
    with col1:
        approved = by_status.get("approved", 0)
        progress = approved / total if total > 0 else 0
        
        st.progress(
            progress,
            text=f"{approved}/{total} aprobadas"
        )
    
    with col2:
        status_emoji = "✅" if polygon_summary.get("approved") else "⏳"
        st.metric("Estado", status_emoji, label_visibility="collapsed")
    
    # Breakdown
    st.markdown("#### Desglose")
    
    cols = st.columns(len(by_status))
    
    for idx, (status, count) in enumerate(by_status.items()):
        with cols[idx]:
            status_label = {
                "pending": "⏳ Pendiente",
                "approved": "✅ Aprobada",
                "rejected": "❌ Rechazada",
                "needs_revision": "⚠️ Revisar"
            }.get(status, status)
            
            st.metric(status_label, count)


def show_validator_leaderboard(validators_stats: list):
    """Muestra ranking de validadores"""
    st.subheader("🏆 Top Validadores")
    
    if not validators_stats:
        st.info("No hay datos")
        return
    
    df = pd.DataFrame(validators_stats)
    df = df.sort_values("validations_count", ascending=False).head(10)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👤 Validador", df.iloc[0]["name"] if len(df) > 0 else "—")
    
    with col2:
        st.metric("✅ Validaciones", df.iloc[0]["validations_count"] if len(df) > 0 else 0)
    
    with col3:
        avg_score = df.iloc[0]["avg_score"] if len(df) > 0 else 0
        st.metric("📊 Score Promedio", f"{avg_score:.1f}")
    
    st.markdown("---")
    
    # Tabla
    display_df = df[["name", "validations_count", "avg_score", "approval_rate"]].copy()
    display_df.columns = ["Validador", "Validaciones", "Score Promedio", "% Aprobadas"]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def show_timeline_chart(validations_by_date: dict):
    """Muestra línea de tiempo de validaciones"""
    st.subheader("📈 Validaciones por Día")
    
    if not validations_by_date:
        st.info("No hay datos")
        return
    
    df = pd.DataFrame([
        {"Fecha": date, "Validaciones": count}
        for date, count in validations_by_date.items()
    ])
    
    fig = px.line(
        df,
        x="Fecha",
        y="Validaciones",
        markers=True,
        title="Actividad de Validación",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
