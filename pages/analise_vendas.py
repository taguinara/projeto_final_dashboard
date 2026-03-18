import streamlit as st
import pandas as pd
import plotly.express as px

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

def carregar_dados():
    # Carregar os dados de vendas
    # Pequena correção: Garanti que o caminho do arquivo seja acessível
    df = pd.read_csv('dados/vendas.csv')
    df['Data'] = pd.to_datetime(df["Data"])
    return df

# Função para formatação brasileira (conforme o visão_geral)
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Utiliza a função para carregar os dados
dados_vendas = carregar_dados()

st.title(":moneybag: Análise Detalhada de Vendas")

# Filtros para análise
st.sidebar.header("Filtros de Vendas")

regioes = st.sidebar.multiselect(
    "Selecione as Regiões",
    options=dados_vendas["Região"].unique(),
    default=dados_vendas["Região"].unique()
)

categorias = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=dados_vendas["Categoria"].unique(),
    default=dados_vendas["Categoria"].unique()
)

data_min = dados_vendas["Data"].min().date()
data_max = dados_vendas["Data"].max().date()

data_range = st.sidebar.date_input(
    "Selecione o Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

# Lógica de filtragem
if len(data_range) == 2:
    start_date, end_date = data_range
    dados_filtrados = dados_vendas[
        (dados_vendas["Região"].isin(regioes)) &
        (dados_vendas["Categoria"].isin(categorias)) &
        (dados_vendas["Data"].dt.date.between(start_date, end_date))
    ]
else:
    dados_filtrados = dados_vendas

# --- MÉTRICAS FILTRADAS COM SETAS E FORMATAÇÃO ---
col1, col2, col3 = st.columns(3)

receita_total = dados_filtrados['Vendas'].sum()
lucro_total = dados_filtrados['Lucro'].sum()

# CORREÇÃO: Adicionado formatação e Deltas (setas verdes/vermelhas)
col1.metric("Receita filtrada", formatar_real(receita_total), delta="Vendas")
col2.metric("Lucro filtrado", formatar_real(lucro_total), delta="Lucro")

margem_media = 0.0
if receita_total > 0:
    margem_media = (lucro_total / receita_total * 100)

col3.metric("Margem média", f"{margem_media:.2f}%", delta="Margem")

st.divider()

# --- PERFORMANCE POR VENDEDOR ---
st.subheader(":busts_in_silhouette: Performance por Vendedor")
vendas_vendedor = dados_filtrados.groupby("Vendedor").agg(
    Receita=("Vendas", "sum"),
    Lucro=("Lucro", "sum"),
    Transações=("Vendas", "count"),
    Ticket_Médio=("Vendas", "mean"),
).round(2).sort_values(by="Receita", ascending=False)

v_col1, v_col2 = st.columns(2)

with v_col1:
    st.markdown("#### Tabela de dados por Vendedor")
    st.dataframe(vendas_vendedor, use_container_width=True)

with v_col2:
    fig_vend = px.bar(
        vendas_vendedor.reset_index(),
        x="Vendedor",
        y="Receita",
        title="Receita e Lucro por Vendedor",
        color="Lucro",
        color_continuous_scale=px.colors.sequential.Blues,
    )
    
    # CORREÇÃO: Ajuste de cores do gráfico para não sumir no fundo
    fig_vend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#3F3FD4"
    )
    st.plotly_chart(fig_vend, use_container_width=True)

# --- ANÁLISE TEMPORAL ---
st.subheader(":calendar: Análise Temporal")  

# CORREÇÃO: Adicionado copy() para evitar SettingWithCopyWarning
dados_filtrados = dados_filtrados.copy()
dados_filtrados['Mês'] = dados_filtrados["Data"].dt.to_period('M').astype(str)
mensal = dados_filtrados.groupby('Mês').agg(
    Receita=('Vendas', 'sum'),
    Lucro=('Lucro', 'sum'),
).reset_index()

fig_temp = px.bar(
    mensal, x='Mês', y=['Receita', 'Lucro'],
    barmode='group', 
    title='Receita X Lucro Mensal',
    color_discrete_sequence=['#3F3FD4', '#1E90FF'] # Tons de azul
)

# CORREÇÃO: Ajuste visual para transparência e cores dos textos
fig_temp.update_layout(
    xaxis_tickangle=-45,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color="#3F3FD4",
    legend_title_font_color="#3F3FD4"
)

st.plotly_chart(fig_temp, use_container_width=True)
