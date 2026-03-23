import streamlit as st
import pandas as pd

st.markdown("""
<style>
    .stApp {
        background-color: #191970;
    }
    h1, h2, h3, h4, h5, h6, span, p, label, .stMetric div {
        color: #FFFFFF !important;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)


st.title("ℹ️ Sobre o Sistema")
st.subheader("Dashboard Profissional desenvolvido em Streamlit.")
st.markdown("""
Dashboard desenvolvido como projeto integrador do curso de Streamlit.\n  
***Tecnologias utilizadas:***\n  
- Streamlit: Framework para apps web em Python\n
- Pandas: Manipulação e análise de dados\n
- Plotly Express: Visualizações interativas\n
- NumPy: Geração de dados numéricos\n
Funcionalidades:\n
📊 Visão geral com KPIs e gráficos resumo\n
💰 Análise detalhada de vendas com filtros\n
📦 Análise individual por produto\n
📥 Download de dados filtrados\n
""")
st.markdown("---") 