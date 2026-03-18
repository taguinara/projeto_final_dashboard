import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Análise de Produtos")

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

# Carregar dados
dados_vendas = pd.read_csv('dados/vendas.csv')

# Selectbox
option = st.selectbox(
    "Selecione um produto",
    ("Headphone", "Headset", "Memoria RAM", "Mouse", "SSD", "Teclado", "Webcam")
)

# Filtrar dados
dados_filtrados = dados_vendas[dados_vendas['Produto'] == option]

# Colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    receita = dados_filtrados['Vendas'].sum()
    st.metric("Receita", f"R$ {receita:,.2f}")

with col2:
    lucro = dados_filtrados['Lucro'].sum()
    st.metric("Lucro", f"R$ {lucro:,.2f}")

with col3:
    qtd = dados_filtrados['Quantidade'].sum()
    st.metric("Qtd. Vendida", qtd)

with col4:
    preco_medio = receita / qtd if qtd != 0 else 0
    st.metric("Preço Médio", f"R$ {preco_medio:,.2f}")


