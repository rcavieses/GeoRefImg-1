import streamlit as st

def show_kpi_card(label: str, value, delta=None, emoji="", help_text=""):
    """Muestra tarjeta KPI mejorada"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.metric(label, value, delta, help=help_text)
    
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 32px'>{emoji}</div>", 
                   unsafe_allow_html=True)

def show_kpi_row(metrics: list):
    """Muestra fila de KPIs"""
    cols = st.columns(len(metrics))
    
    for idx, (col, metric) in enumerate(zip(cols, metrics)):
        with col:
            st.metric(
                metric.get("label", "—"),
                metric.get("value", "—"),
                metric.get("delta", None),
                help=metric.get("help", "")
            )

def show_status_card(status: str, count: int, percentage: float = 0):
    """Muestra tarjeta de estado"""
    status_config = {
        "approved": {"color": "#28a745", "emoji": "✅"},
        "rejected": {"color": "#dc3545", "emoji": "❌"},
        "pending": {"color": "#ffc107", "emoji": "⏳"},
        "needs_revision": {"color": "#fd7e14", "emoji": "⚠️"}
    }
    
    config = status_config.get(status, {"color": "#6c757d", "emoji": "?"})
    
    st.markdown(f"""
        <div style="
            background-color: {config['color']}20;
            border-left: 4px solid {config['color']};
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        ">
            <h3 style="margin: 0; color: {config['color']}">
                {config['emoji']} {status.replace('_', ' ').title()}
            </h3>
            <p style="margin: 5px 0; font-size: 24px; font-weight: bold">{count}</p>
            <p style="margin: 0; font-size: 12px; color: #666">{percentage:.1f}%</p>
        </div>
    """, unsafe_allow_html=True)
