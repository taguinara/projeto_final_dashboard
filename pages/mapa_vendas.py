# Métricas 
# Distribuição geográfica
# Resumo por cidades
# Filtros por região

import streamlit as st
import pandas as pd

# 1. Configuração de Estilo (Mantendo a identidade visual profissional)
st.markdown("""
    <style>
        .stApp {
            background-color: #191970; /* Midnight Blue */
        }
        h1, h2, h3, h4, h5, h6, span, p, label, .stMetric div {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("📍 Mapa de Vendas por Localização")
st.subheader("Visualize a distribuição das vendas e aplique filtros para explorar os dados.")

a, b = st.columns(2)
c, d = st.columns(2)

a.metric("Temperature", "30°F", "-9°F", border=True)
b.metric("Wind", "4 mph", "2 mph", border=True)

c.metric("Humidity", "77%", "5%", border=True)
d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)
