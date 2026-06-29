import streamlit as st
import pandas as pd
from app.ui.session_manager import SessionManager
from app.ui.components.validation_dashboard import (
    show_validation_stats,
    show_validation_chart,
    show_validation_progress
)
from app.database import SessionLocal
from app.services.validation_service import ValidationService

@SessionManager.require_auth
def show_validations():
    """Pagina principal de validaciones"""
    user = SessionManager.get_current_user()
    user_id = SessionManager.get_user_id()
    
    st.title("✅ Sistema de Validaciones")
    st.markdown("Valida poligonos y supervisa el progreso")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "🎯 Por Hacer",
        "✔️ Validar",
        "📊 Dashboard"
    ])
    
    db = SessionLocal()
    
    try:
        # TAB 1: PENDIENTES
        with tab1:
            st.subheader("Poligonos Pendientes")
            
            pending = ValidationService.get_pending_validations(db, limit=20)
            
            if pending:
                st.metric("Total Pendientes", len(pending))
                st.divider()
                
                pending_data = []
                for val in pending:
                    pending_data.append({
                        "ID": val.id,
                        "Poligono": val.polygon_id,
                        "Estado": val.status,
                        "Tipo": val.validation_type or "—"
                    })
                
                df = pd.DataFrame(pending_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            else:
                st.success("Sin validaciones pendientes")
        
        # TAB 2: VALIDAR
        with tab2:
            st.subheader("Realizar Validacion")
            
            col1, col2 = st.columns(2)
            
            with col1:
                polygon_id = st.number_input("ID del Poligono", min_value=0, step=1)
            
            with col2:
                validation_type = st.selectbox(
                    "Tipo de Validacion",
                    ["topology", "accuracy", "completeness", "manual"]
                )
            
            st.divider()
            
            with st.form("validation_form"):
                status = st.selectbox(
                    "Estado",
                    ["approved", "rejected", "needs_revision", "pending"]
                )
                
                score = st.slider("Puntuacion", 0, 100, 75)
                notes = st.text_area("Notas", height=150)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submit = st.form_submit_button("Enviar", use_container_width=True, type="primary")
                
                with col2:
                    st.form_submit_button("Cancelar", use_container_width=True)
                
                if submit:
                    try:
                        validation = ValidationService.create_validation(
                            db=db,
                            polygon_id=polygon_id,
                            validator_id=user_id,
                            status=status,
                            validation_type=validation_type,
                            score=score,
                            notes=notes
                        )
                        st.success(f"Validacion #{validation.id} creada")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # TAB 3: DASHBOARD
        with tab3:
            st.subheader("Dashboard de Validaciones")
            
            stats = ValidationService.get_validation_stats(db)
            show_validation_stats(stats)
            
            st.divider()
            show_validation_chart(stats)
    
    finally:
        db.close()
    
    st.markdown("---")
    st.caption(f"Sesion: {user['username']}")
