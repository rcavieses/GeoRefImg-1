import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.ui.session_manager import SessionManager
from app.ui.components.dashboard_cards import show_status_card
from app.database import SessionLocal
from app.services.report_service import ReportService
from app.models.validation import Validation
from sqlalchemy import func

@SessionManager.require_auth
def show_dashboard():
    """Dashboard principal del sistema"""
    user = SessionManager.get_current_user()

    # Reducir tamaño de texto un 20%
    st.markdown("""
        <style>
            h1 { font-size: 28px !important; }
            h2 { font-size: 22.4px !important; }
            h3 { font-size: 19.2px !important; }
            h4 { font-size: 16px !important; }
            p { font-size: 13.6px !important; }
            .metric-value { font-size: 20px !important; }
            .metric-label { font-size: 12px !important; }
            .caption { font-size: 11.2px !important; }
            .info-box { font-size: 13.6px !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Dashboard de Validación")
    st.markdown("Resumen completo de validaciones y actividad del sistema")

    db = SessionLocal()

    try:
        overview = ReportService.get_system_overview(db)
        user_stats = ReportService.get_user_stats(db, SessionManager.get_user_id())
        top_validators = ReportService.get_top_validators(db, limit=5)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 General",
            "👤 Mi Actividad",
            "🏆 Top Validadores",
            "📋 Validaciones",
            "🎨 Polígonos Dibujados",
            "📊 Resumen"
        ])

        # TAB 1: Resumen General
        with tab1:
            st.subheader("Resumen General del Sistema")

            col1, col2, col3 = st.columns(3)

            with col1:
                total_polygons = overview.get("total_polygons", 0)
                st.metric("📍 Polígonos Total", total_polygons)

            with col2:
                total_validations = overview.get("total_validations", 0)
                st.metric("✅ Validaciones", total_validations)

            with col3:
                total_users = overview.get("total_users", 0)
                st.metric("👥 Usuarios", total_users)

            st.divider()

            # Estados de validación
            st.subheader("Estados de Validación")

            by_status = overview.get("validations_by_status", {})

            if by_status:
                col1, col2 = st.columns(2)

                with col1:
                    # Gráfico de pastel
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
                    # Estadísticas detalladas
                    st.markdown("**Distribución por Estado**")
                    total = sum(by_status.values())
                    for status, count in by_status.items():
                        percentage = (count / total * 100) if total > 0 else 0
                        st.metric(
                            f"{status.title()}",
                            f"{count} ({percentage:.1f}%)"
                        )

            st.divider()

            # Estadísticas adicionales
            col1, col2, col3 = st.columns(3)

            with col1:
                approval_rate = overview.get('approval_rate', 0)
                st.metric("✅ Tasa de Aprobación", f"{approval_rate:.1f}%")

            with col2:
                rejected_rate = 100 - approval_rate if approval_rate else 0
                st.metric("❌ Tasa de Rechazo", f"{rejected_rate:.1f}%")

            with col3:
                avg_score = overview.get('average_validation_score', 0)
                st.metric("⭐ Score Promedio", f"{avg_score:.1f}")

        # TAB 2: Mi Actividad
        with tab2:
            st.subheader(f"Mi Actividad - {user['username']}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📍 Polígonos Dibujados",
                    user_stats.get("polygons_created", 0)
                )

            with col2:
                st.metric(
                    "✅ Validaciones Realizadas",
                    user_stats.get("validations_done", 0)
                )

            with col3:
                st.metric(
                    "⭐ Score Promedio",
                    f"{user_stats.get('average_score', 0):.1f}"
                )

            st.divider()

            # Mis validaciones recientes
            st.subheader("Mis Validaciones Recientes")

            my_validations = db.query(Validation).filter(
                Validation.validator_id == SessionManager.get_user_id()
            ).order_by(Validation.created_at.desc()).limit(10).all()

            if my_validations:
                validation_data = []
                for v in my_validations:
                    validation_data.append({
                        "Polígono ID": v.polygon_id,
                        "Estado": v.status.upper(),
                        "Tipo": v.validation_type or "N/A",
                        "Fecha": v.created_at.strftime("%Y-%m-%d %H:%M"),
                        "Notas": v.notes or "-"
                    })

                df = pd.DataFrame(validation_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No hay validaciones realizadas aún")

        # TAB 3: Top Validadores
        with tab3:
            st.subheader("🏆 Top Validadores")

            if top_validators:
                # Crear DataFrame
                validator_data = []
                for validator in top_validators:
                    validator_data.append({
                        "Usuario": validator.get("username", "N/A"),
                        "Validaciones": validator.get("validations_count", 0),
                        "Score Promedio": f"{validator.get('average_score', 0):.1f}"
                    })

                df = pd.DataFrame(validator_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Gráfico de top validadores
                if len(validator_data) > 0:
                    usernames = [v["Usuario"] for v in validator_data]
                    validations = [v["Validaciones"] for v in validator_data]

                    fig = go.Figure(data=[
                        go.Bar(
                            x=usernames,
                            y=validations,
                            marker_color='rgba(55, 128, 191, 0.7)'
                        )
                    ])
                    fig.update_layout(
                        title="Validaciones por Usuario",
                        xaxis_title="Usuario",
                        yaxis_title="Número de Validaciones",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sin datos de validadores")

        # TAB 4: Validaciones Recientes
        with tab4:
            st.subheader("📋 Validaciones Recientes del Sistema")

            recent_validations = db.query(Validation).order_by(
                Validation.created_at.desc()
            ).limit(20).all()

            if recent_validations:
                validation_data = []
                for v in recent_validations:
                    validation_data.append({
                        "Polígono ID": v.polygon_id,
                        "Usuario": f"ID: {v.validator_id}",
                        "Estado": v.status.upper(),
                        "Tipo": v.validation_type or "manual",
                        "Fecha": v.created_at.strftime("%Y-%m-%d %H:%M"),
                        "Notas": v.notes[:50] + "..." if v.notes and len(v.notes) > 50 else (v.notes or "-")
                    })

                df = pd.DataFrame(validation_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Gráfico de validaciones por día
                st.divider()
                st.subheader("📈 Validaciones por Día")

                daily_validations = db.query(
                    func.date(Validation.created_at).label('date'),
                    func.count(Validation.id).label('count')
                ).group_by(
                    func.date(Validation.created_at)
                ).order_by('date').all()

                if daily_validations:
                    dates = [str(v[0]) for v in daily_validations]
                    counts = [v[1] for v in daily_validations]

                    fig = go.Figure(data=[
                        go.Scatter(
                            x=dates,
                            y=counts,
                            mode='lines+markers',
                            name='Validaciones',
                            line=dict(color='#1f77b4', width=2),
                            marker=dict(size=8)
                        )
                    ])
                    fig.update_layout(
                        title="Actividad de Validaciones",
                        xaxis_title="Fecha",
                        yaxis_title="Número de Validaciones",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sin validaciones registradas aún")

    finally:
        db.close()

    # TAB 5: Polígonos Dibujados
    with tab5:
        st.subheader("🎨 Polígonos Dibujados por Usuarios")

        st.info("""
            Muestra los polígonos que han sido dibujados manualmente por los usuarios
            con su justificación y fecha de creación.
        """)

        # Simulación de datos de polígonos dibujados (desde session_state)
        drawn_polygons = st.session_state.get("drawn_polygons", [])

        if drawn_polygons:
            st.markdown(f"**Total dibujados: {len(drawn_polygons)}**")

            for i, poly in enumerate(drawn_polygons):
                with st.expander(f"📍 Polígono {i+1}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Nombre:** {poly.get('name', 'Sin nombre')}")
                    with col2:
                        st.markdown(f"**Usuario:** ID {st.session_state.get('user_id')}")

                    st.markdown("**Justificación:**")
                    st.text(poly.get('justification', 'N/A'))

                    st.caption(f"📅 Creado: {poly.get('timestamp', 'N/A')}")
        else:
            st.info("No hay polígonos dibujados aún")

    # TAB 6: Resumen Completo
    with tab6:
        st.subheader("📊 Resumen Completo de Actividad")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "✅ Validaciones",
                overview.get("total_validations", 0),
                "acumuladas"
            )

        with col2:
            drawn_count = len(st.session_state.get("drawn_polygons", []))
            st.metric(
                "🎨 Polígonos Dibujados",
                drawn_count,
                "creados"
            )

        st.divider()

        # Actividad por usuario
        st.subheader("👥 Actividad por Usuario")

        user_activity = db.query(
            Validation.validator_id,
            func.count(Validation.id).label('validations_count')
        ).group_by(Validation.validator_id).order_by(
            func.count(Validation.id).desc()
        ).limit(10).all()

        if user_activity:
            activity_data = []
            for user_id, count in user_activity:
                activity_data.append({
                    "Usuario ID": user_id,
                    "Validaciones": count
                })

            df = pd.DataFrame(activity_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay actividad registrada")

        st.divider()

        # Gráfico de actividad general
        st.subheader("📈 Tendencia de Validaciones")

        daily_data = db.query(
            func.date(Validation.created_at).label('date'),
            func.count(Validation.id).label('count')
        ).group_by(func.date(Validation.created_at)).order_by('date').all()

        if daily_data:
            dates = [str(d[0]) for d in daily_data]
            counts = [d[1] for d in daily_data]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=counts,
                mode='lines+markers',
                name='Validaciones',
                line=dict(color='#1f77b4', width=2)
            ))
            fig.update_layout(
                title="Validaciones a lo Largo del Tiempo",
                xaxis_title="Fecha",
                yaxis_title="Cantidad",
                height=300,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.caption(f"Dashboard | {user['username']} | {user['role'].upper()}")
