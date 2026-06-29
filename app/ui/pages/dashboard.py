import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.ui.session_manager import SessionManager
from app.ui.components.dashboard_cards import show_status_card
from app.database import SessionLocal
from app.services.report_service import ReportService

@SessionManager.require_auth
def show_dashboard():
    """Dashboard principal del sistema"""
    user = SessionManager.get_current_user()
    
    st.title("Dashboard Principal")
    st.markdown("Resumen global del sistema")
    
    db = SessionLocal()
    
    try:
        overview = ReportService.get_system_overview(db)
        user_stats = ReportService.get_user_stats(db, SessionManager.get_user_id())
        top_validators = ReportService.get_top_validators(db, limit=5)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "General", "Mi Perfil", "Validadores", "Reportes"
        ])
        
        with tab1:
            st.subheader("Resumen General")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Poligonos", overview.get("total_polygons", 0))
            with col2:
                st.metric("Validaciones", overview.get("total_validations", 0))
            with col3:
                st.metric("Anotaciones", overview.get("total_annotations", 0))
            with col4:
                st.metric("Usuarios", overview.get("total_users", 0))
            
            st.divider()
            
            st.subheader("Estados de Validacion")
            
            by_status = overview.get("validations_by_status", {})
            
            if by_status:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure(data=[
                        go.Pie(
                            labels=list(by_status.keys()),
                            values=list(by_status.values()),
                            hole=0.3
                        )
                    ])
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    total = sum(by_status.values())
                    for status, count in by_status.items():
                        percentage = (count / total * 100) if total > 0 else 0
                        show_status_card(status, count, percentage)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Score Promedio", 
                         f"{overview.get('average_validation_score', 0):.1f}")
            with col2:
                st.metric("Aprobadas", 
                         f"{overview.get('approval_rate', 0):.1f}%")
        
        with tab2:
            st.subheader(f"Mi Actividad - {user['username']}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Poligonos", user_stats.get("polygons_created", 0))
            with col2:
                st.metric("Validaciones", user_stats.get("validations_done", 0))
            with col3:
                st.metric("Anotaciones", user_stats.get("annotations_created", 0))
            with col4:
                st.metric("Score", f"{user_stats.get('average_score', 0):.1f}")
        
        with tab3:
            st.subheader("Top Validadores")
            
            if top_validators:
                df = pd.DataFrame(top_validators)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("Sin datos")
        
        with tab4:
            st.subheader("Exportar Reportes")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Excel", use_container_width=True):
                    st.success("En preparacion...")
            with col2:
                if st.button("PDF", use_container_width=True):
                    st.success("En preparacion...")
    
    finally:
        db.close()
    
    st.markdown("---")
    st.caption(f"Dashboard | {user['username']}")
